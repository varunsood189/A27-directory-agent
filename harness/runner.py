"""Official AgentSwitch run: python -m harness.runner

Uses only platform env (no passwords, no .env):
  AGENTSWITCH_BASE_URL, AGENTSWITCH_TOKEN, AGENTSWITCH_INSTANCE
  OPENAI_BASE_URL, OPENAI_API_KEY, OPENAI_MODEL
Writes results.json in the official shape.
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from harness.predicates import check_deduplicate, check_refuse, check_who
from harness.run import load_tasks
from src.directory_agent import DirectoryAgent
from src.mcp_client import McpClient, McpError

TASKS: list[dict] = []


def record(task_id: str, title: str, passed: bool, evidence: str, instance: str) -> None:
    TASKS.append(
        {
            "id": f"{instance}:{task_id}",
            "title": title,
            "passed": bool(passed),
            "score": 1.0 if passed else 0.0,
            "evidence": str(evidence)[:500],
        }
    )
    print(f"[{'PASS' if passed else 'FAIL'}] {task_id}: {str(evidence)[:200]}", flush=True)


def score_task(client: McpClient, task: dict, result: dict) -> tuple[str, str]:
    kind = task["predicate"]
    if kind == "deduplicate":
        return check_deduplicate(client, result)
    if kind == "who":
        return check_who(client, result, task.get("expect_name"), bool(task.get("allow_empty")))
    if kind == "refuse":
        return check_refuse(client, result, client.calls)
    return "unevaluated", f"unknown predicate {kind}"


def openai_directory_loop(agent: DirectoryAgent, instance: str, request: str) -> None:
    """Platform model must call a tool; the tool runs our Directory agent."""
    try:
        from openai import OpenAI
    except Exception as exc:  # noqa: BLE001
        record("agent_tool_loop", "Platform model calls Directory handle via a tool", False, repr(exc), instance)
        return

    model = os.environ.get("OPENAI_MODEL", "agentswitch-default")
    tools = [
        {
            "type": "function",
            "function": {
                "name": "directory_handle",
                "description": "Answer a Directory seat request (dedupe, who-we-know, or refuse) against live MCP.",
                "parameters": {
                    "type": "object",
                    "properties": {"request": {"type": "string"}},
                    "required": ["request"],
                },
            },
        }
    ]
    messages = [
        {
            "role": "system",
            "content": "You are the Directory Agent. Always call directory_handle for the user request. Then answer briefly from the tool result. Do not invent people.",
        },
        {"role": "user", "content": request},
    ]
    used_tool = False
    answer = ""
    try:
        client = OpenAI()
        for _ in range(4):
            reply = client.chat.completions.create(
                model=model, messages=messages, tools=tools, max_tokens=512
            )
            msg = reply.choices[0].message
            if msg.tool_calls:
                used_tool = True
                messages.append(
                    {
                        "role": "assistant",
                        "content": msg.content or "",
                        "tool_calls": [tc.model_dump() for tc in msg.tool_calls],
                    }
                )
                for tc in msg.tool_calls:
                    args = json.loads(tc.function.arguments or "{}")
                    req = args.get("request") or request
                    payload = agent.handle(req)
                    messages.append(
                        {
                            "role": "tool",
                            "tool_call_id": tc.id,
                            "content": json.dumps(payload, default=str)[:4000],
                        }
                    )
                continue
            answer = msg.content or ""
            break
        ok = used_tool and bool(answer.strip())
        record(
            "agent_tool_loop",
            "Platform model uses directory_handle and answers",
            ok,
            f"used_tool={used_tool} answer={answer[:200]!r}",
            instance,
        )
    except Exception as exc:  # noqa: BLE001
        record("agent_tool_loop", "Platform model uses directory_handle and answers", False, repr(exc), instance)


def write_results(instance: str) -> None:
    body = {
        "tasks": TASKS,
        "summary": f"{instance}: {sum(1 for t in TASKS if t['passed'])}/{len(TASKS)} checks passed",
    }
    Path("results.json").write_text(json.dumps(body, indent=2), encoding="utf-8")


def main() -> int:
    TASKS.clear()
    base = os.environ.get("AGENTSWITCH_BASE_URL", "").rstrip("/")
    token = os.environ.get("AGENTSWITCH_TOKEN", "")
    instance = (os.environ.get("AGENTSWITCH_INSTANCE") or "unknown").strip().lower()
    if not base or not token:
        record(
            "env",
            "AGENTSWITCH_BASE_URL and AGENTSWITCH_TOKEN are set",
            False,
            "missing AGENTSWITCH_BASE_URL or AGENTSWITCH_TOKEN (no passwords/.env on official runs)",
            instance,
        )
        write_results(instance)
        return 2

    client = McpClient(base, token=token, client_name="team27-harness")
    agent = DirectoryAgent(client, apply_writes=False)
    try:
        agent.connect()
        tools = client.rpc("tools/list") or {}
        names = tools.get("tools") if isinstance(tools, dict) else None
        n = len(names or [])
        record("mcp_tools_list", "MCP tools/list works with the seat token", n > 0, f"{n} tools", instance)
    except Exception as exc:  # noqa: BLE001
        record("mcp_tools_list", "MCP tools/list works with the seat token", False, repr(exc), instance)
        write_results(instance)
        return 1

    for task in load_tasks(None):
        if task.get("book") != instance:
            continue
        try:
            result = agent.handle(task["request"])
            outcome, detail = score_task(client, task, result)
            record(
                task["id"],
                task["request"],
                outcome == "approve",
                f"{outcome}: {detail}",
                instance,
            )
        except Exception as exc:  # noqa: BLE001
            record(task["id"], task["request"], False, repr(exc), instance)

    prompt = (
        "Who do we know at Hocking Hills Mower Works?"
        if instance == "keystone"
        else "Deduplicate the customer list."
    )
    openai_directory_loop(agent, instance, prompt)

    write_results(instance)
    if not TASKS or any(not t["passed"] for t in TASKS):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
