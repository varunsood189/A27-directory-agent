"""Read-only Directory dump: Party, relationships, address books."""

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

PROTOCOL = "2025-11-25"
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "live"


def http_json(method: str, url: str, token: str | None = None, body: dict | None = None):
    data = None if body is None else json.dumps(body).encode()
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            raw = resp.read().decode()
            if not raw.strip():
                return resp.status, {}
            return resp.status, json.loads(raw)
    except urllib.error.HTTPError as e:
        raw = e.read().decode()
        try:
            return e.code, json.loads(raw)
        except json.JSONDecodeError:
            return e.code, raw


def mcp_call(base, token, rpc_id, name, arguments=None):
    status, payload = http_json(
        "POST",
        f"{base}/api/mcp",
        token=token,
        body={
            "jsonrpc": "2.0",
            "id": rpc_id,
            "method": "tools/call",
            "params": {"name": name, "arguments": arguments or {}},
        },
    )
    return status, payload


def unwrap(payload: dict) -> dict:
    if not isinstance(payload, dict):
        return {}
    if "result" in payload and isinstance(payload["result"], dict):
        sc = payload["result"].get("structuredContent")
        if isinstance(sc, dict):
            return sc
        content = payload["result"].get("content") or []
        if content and isinstance(content[0], dict) and "text" in content[0]:
            try:
                return json.loads(content[0]["text"])
            except json.JSONDecodeError:
                return payload["result"]
        return payload["result"]
    return payload


def dump_book(name: str, base: str, email: str, password: str) -> None:
    dest = OUT / name
    dest.mkdir(parents=True, exist_ok=True)
    st, login = http_json("POST", f"{base}/api/auth/login", body={"email": email, "password": password})
    if st != 200 or not isinstance(login, dict) or "token" not in login:
        raise SystemExit(f"{name} login {st}")
    token = login["token"]
    http_json(
        "POST",
        f"{base}/api/mcp",
        token=token,
        body={
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": PROTOCOL,
                "capabilities": {},
                "clientInfo": {"name": "team27-directory-dump", "version": "0.1"},
            },
        },
    )
    http_json(
        "POST",
        f"{base}/api/mcp",
        token=token,
        body={"jsonrpc": "2.0", "method": "notifications/initialized", "params": {}},
    )

    summary = {}
    rpc = 10
    for tool, args, key in [
        ("Party.list", {"limit": 20, "sort_by": "name", "sort_order": "asc"}, "party"),
        ("Party.list", {"limit": 20, "type": "organization"}, "party_orgs"),
        ("Party.list", {"limit": 20, "contact_type": "customer"}, "party_customers"),
        ("PartyRelationship.list", {"limit": 20}, "relationships"),
        ("AddressBook.list", {"limit": 20}, "address_books"),
        ("AddressBookEntry.list", {"limit": 20}, "address_book_entries"),
        ("ContactGroup.list", {"limit": 20}, "contact_groups"),
        ("ContactGroupMember.list", {"limit": 20}, "contact_group_members"),
        ("Company.list", {"limit": 5}, "companies"),
    ]:
        st, payload = mcp_call(base, token, rpc, tool, args)
        rpc += 1
        data = unwrap(payload) if st == 200 else {"http": st, "body": payload}
        slim_path = dest / f"dir_{key}.json"
        slim_path.write_text(json.dumps(data, indent=2, default=str)[:200000])
        total = data.get("total") if isinstance(data, dict) else None
        err = None
        if isinstance(payload, dict) and "error" in payload:
            err = payload["error"]
        summary[key] = {"http": st, "total": total, "error": err}
        print(f"{name} {key} http={st} total={total} err={bool(err)}")

    (dest / "directory_summary.json").write_text(json.dumps(summary, indent=2, default=str))


def main() -> None:
    email = os.environ["AS_EMAIL"]
    dump_book("suryodaya", os.environ["AS_SURYODAYA"].rstrip("/"), email, os.environ["AS_PASSWORD_SURYODAYA"])
    dump_book("keystone", os.environ["AS_KEYSTONE"].rstrip("/"), email, os.environ["AS_PASSWORD_KEYSTONE"])


if __name__ == "__main__":
    try:
        main()
    except KeyError as e:
        print(f"missing env {e}", file=sys.stderr)
        sys.exit(2)
