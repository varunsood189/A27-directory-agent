"""Harness: journal the run to disk, then score from live MCP rows."""

from __future__ import annotations

import argparse
import json
import os
import sys
import traceback
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from harness.predicates import check_deduplicate, check_refuse, check_who
from src.directory_agent import DirectoryAgent
from src.mcp_client import McpClient

BOOK_URL = {
    "suryodaya": os.environ.get("AS_SURYODAYA", "https://agentswitch.theschoolofai.in"),
    "keystone": os.environ.get("AS_KEYSTONE", "https://class.agentswitch.theschoolofai.in"),
}
BOOK_PASS = {
    "suryodaya": "AS_PASSWORD_SURYODAYA",
    "keystone": "AS_PASSWORD_KEYSTONE",
}


def load_tasks(only: str | None) -> list[dict]:
    folder = ROOT / "harness" / "tasks"
    tasks = []
    for path in sorted(folder.glob("*.json")):
        task = json.loads(path.read_text())
        if only and task.get("id") != only:
            continue
        tasks.append(task)
    return tasks


def score(client: McpClient, task: dict, result: dict) -> tuple[str, str]:
    kind = task["predicate"]
    if kind == "deduplicate":
        return check_deduplicate(client, result)
    if kind == "who":
        return check_who(
            client,
            result,
            task.get("expect_name"),
            bool(task.get("allow_empty")),
        )
    if kind == "refuse":
        return check_refuse(client, result, client.calls)
    return "unevaluated", f"unknown predicate {kind}"


def run_task(task: dict, email: str) -> dict:
    book = task["book"]
    password = os.environ.get(BOOK_PASS[book])
    if not password:
        return {
            "task_id": task["id"],
            "outcome": "unevaluated",
            "detail": f"missing env {BOOK_PASS[book]}",
        }
    client = McpClient(BOOK_URL[book], email, password, client_name="team27-harness")
    agent = DirectoryAgent(client, apply_writes=os.environ.get("APPLY_WRITES") == "1")
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    run_dir = ROOT / "runs" / book / task["id"]
    run_dir.mkdir(parents=True, exist_ok=True)
    journal_path = run_dir / f"{stamp}.json"
    payload: dict = {
        "task_id": task["id"],
        "task": task,
        "started_at": stamp,
        "outcome": "unevaluated",
        "detail": "not yet scored",
        "result": None,
        "calls": [],
    }
    try:
        me = agent.connect()
        payload["me"] = {"email": me.get("email"), "allowed_apps": me.get("allowed_apps"), "roles": me.get("roles")}
        result = agent.handle(task["request"])
        payload["result"] = result
        payload["calls"] = client.calls
        journal_path.write_text(json.dumps(payload, indent=2, default=str))
        outcome, detail = score(client, task, result)
        payload["outcome"] = outcome
        payload["detail"] = detail
        payload["calls"] = client.calls
    except Exception as exc:
        payload["outcome"] = "unevaluated"
        payload["detail"] = f"{type(exc).__name__}: {exc}"
        payload["traceback"] = traceback.format_exc()
        payload["calls"] = client.calls
    journal_path.write_text(json.dumps(payload, indent=2, default=str))
    payload["journal"] = str(journal_path)
    return payload


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--task", default=None)
    args = parser.parse_args()
    email = os.environ.get("AS_EMAIL", "team27@theschoolofai.in")
    tasks = load_tasks(args.task)
    if not tasks:
        print("no tasks", file=sys.stderr)
        return 2
    rows = [run_task(task, email) for task in tasks]
    summary = [
        {
            "id": r["task_id"] if "task_id" in r else r.get("task", {}).get("id"),
            "outcome": r.get("outcome"),
            "detail": r.get("detail"),
            "journal": r.get("journal"),
        }
        for r in rows
    ]
    for row in rows:
        if "task_id" not in row and "task" in row:
            row["task_id"] = row["task"]["id"]
    print(json.dumps(summary, indent=2))
    if any(r.get("outcome") == "unevaluated" for r in rows):
        return 3
    if any(r.get("outcome") != "approve" for r in rows):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
