"""JSON-RPC MCP client for AgentSwitch. POST only, no SSE, no batching."""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from typing import Any

PROTOCOL = "2025-11-25"


class McpError(RuntimeError):
    def __init__(self, message: str, *, http_status: int | None = None, payload: Any = None):
        super().__init__(message)
        self.http_status = http_status
        self.payload = payload


class McpClient:
    def __init__(self, base_url: str, email: str, password: str, client_name: str = "team27-directory"):
        self.base_url = base_url.rstrip("/")
        self.email = email
        self.password = password
        self.client_name = client_name
        self.token: str | None = None
        self._rpc_id = 0
        self.calls: list[dict[str, Any]] = []

    def _http(self, method: str, path: str, body: dict | None = None) -> tuple[int, Any]:
        url = f"{self.base_url}{path}"
        data = None if body is None else json.dumps(body).encode()
        headers = {"Accept": "application/json", "Content-Type": "application/json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        req = urllib.request.Request(url, data=data, headers=headers, method=method)
        try:
            with urllib.request.urlopen(req, timeout=180) as resp:
                raw = resp.read().decode()
                parsed: Any = json.loads(raw) if raw.strip() else {}
                return resp.status, parsed
        except urllib.error.HTTPError as e:
            raw = e.read().decode()
            try:
                parsed = json.loads(raw) if raw.strip() else {}
            except json.JSONDecodeError:
                parsed = {"raw": raw[:500]}
            return e.code, parsed

    def login(self) -> None:
        status, payload = self._http(
            "POST",
            "/api/auth/login",
            {"email": self.email, "password": self.password},
        )
        if status != 200 or not isinstance(payload, dict) or "token" not in payload:
            raise McpError(f"login failed HTTP {status}", http_status=status, payload=payload)
        self.token = payload["token"]

    def me(self) -> dict[str, Any]:
        status, payload = self._http("GET", "/api/auth/me")
        if status != 200 or not isinstance(payload, dict):
            raise McpError(f"/api/auth/me HTTP {status}", http_status=status, payload=payload)
        return payload

    def handshake(self) -> dict[str, Any]:
        init = self.rpc(
            "initialize",
            {
                "protocolVersion": PROTOCOL,
                "capabilities": {},
                "clientInfo": {"name": self.client_name, "version": "0.1"},
            },
        )
        self._http(
            "POST",
            "/api/mcp",
            {"jsonrpc": "2.0", "method": "notifications/initialized", "params": {}},
        )
        return init

    def rpc(self, method: str, params: dict[str, Any] | None = None) -> Any:
        self._rpc_id += 1
        body = {"jsonrpc": "2.0", "id": self._rpc_id, "method": method, "params": params or {}}
        status, payload = self._http("POST", "/api/mcp", body)
        record = {"method": method, "http": status, "id": self._rpc_id, "params": params or {}}
        if status != 200:
            record["error"] = payload
            self.calls.append(record)
            raise McpError(f"MCP HTTP {status}", http_status=status, payload=payload)
        if not isinstance(payload, dict):
            record["error"] = payload
            self.calls.append(record)
            raise McpError("MCP non-object response", payload=payload)
        if "error" in payload:
            record["error"] = payload["error"]
            self.calls.append(record)
            raise McpError(f"JSON-RPC error: {payload['error']}", payload=payload)
        record["ok"] = True
        self.calls.append(record)
        return payload.get("result")

    def call_tool(self, name: str, arguments: dict[str, Any] | None = None) -> Any:
        result = self.rpc("tools/call", {"name": name, "arguments": arguments or {}})
        if self.calls:
            self.calls[-1]["tool"] = name
            self.calls[-1]["arguments"] = arguments or {}
        return unwrap_tool_result(result)

    def list_all(self, tool: str, extra: dict[str, Any] | None = None, page_size: int = 100) -> list[dict[str, Any]]:
        extra = dict(extra or {})
        offset = 0
        rows: list[dict[str, Any]] = []
        total = None
        while True:
            args = {**extra, "limit": page_size, "offset": offset}
            payload = self.call_tool(tool, args)
            chunk = payload.get("data") if isinstance(payload, dict) else None
            if not isinstance(chunk, list):
                break
            rows.extend([r for r in chunk if isinstance(r, dict)])
            total = payload.get("total", len(rows))
            offset += len(chunk)
            if not chunk or offset >= int(total or 0):
                break
        return rows


def unwrap_tool_result(result: Any) -> Any:
    if not isinstance(result, dict):
        return result
    structured = result.get("structuredContent")
    if isinstance(structured, dict):
        return structured
    content = result.get("content") or []
    if content and isinstance(content[0], dict) and "text" in content[0]:
        try:
            return json.loads(content[0]["text"])
        except json.JSONDecodeError:
            return result
    if "data" in result or "id" in result:
        return result
    return result
