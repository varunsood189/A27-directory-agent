"""AgentSwitch deploy entry: python -m harness.runner --out results.json"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from harness.run import load_tasks, run_task
from src import settings

KNOWN = ("suryodaya", "keystone")


def selected_instances(cli: str | None) -> list[str]:
    """One book if the platform/env/flag sets it; otherwise both."""
    raw = (cli or os.environ.get("AGENTSWITCH_INSTANCE") or os.environ.get("INSTANCE") or "").strip().lower()
    if raw in KNOWN:
        return [raw]
    return ["suryodaya", "keystone"]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default="results.json")
    parser.add_argument("--instance", default=None)
    args = parser.parse_args()

    instances = selected_instances(args.instance)
    email = os.environ.get("AS_EMAIL") or settings.email()
    tasks = [t for t in load_tasks(None) if t.get("book") in instances]

    rows = []
    for task in tasks:
        payload = run_task(task, email)
        rows.append(
            {
                "id": payload.get("task_id") or task.get("id"),
                "instance": task.get("book"),
                "outcome": payload.get("outcome"),
                "detail": payload.get("detail"),
                "journal": payload.get("journal"),
            }
        )

    out_path = Path(args.out)
    if not out_path.is_absolute():
        out_path = ROOT / out_path
    body = {
        "seat": "directory",
        "team": "27",
        "instances": instances,
        "tasks": rows,
        "passed": bool(rows) and all(r.get("outcome") == "approve" for r in rows),
    }
    out_path.write_text(json.dumps(body, indent=2, default=str), encoding="utf-8")
    print(json.dumps(body, indent=2, default=str))

    if not rows:
        return 2
    if any(r.get("outcome") == "unevaluated" for r in rows):
        return 3
    if any(r.get("outcome") != "approve" for r in rows):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
