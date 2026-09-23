#!/usr/bin/env python3
"""Run the Directory agent against one book."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.directory_agent import DirectoryAgent
from src.mcp_client import McpClient

DEFAULT_REQUEST = "Deduplicate the customer list, and tell me who we know at this company."

BOOKS = {
    "suryodaya": "AS_SURYODAYA",
    "keystone": "AS_KEYSTONE",
}
PASSWORDS = {
    "suryodaya": "AS_PASSWORD_SURYODAYA",
    "keystone": "AS_PASSWORD_KEYSTONE",
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--book", choices=BOOKS, default="suryodaya")
    parser.add_argument("--request", default=DEFAULT_REQUEST)
    parser.add_argument("--apply-writes", action="store_true")
    args = parser.parse_args()

    base = os.environ.get(BOOKS[args.book])
    password = os.environ.get(PASSWORDS[args.book])
    email = os.environ.get("AS_EMAIL", "team27@theschoolofai.in")
    if not base or not password:
        missing = [k for k in (BOOKS[args.book], PASSWORDS[args.book]) if not os.environ.get(k)]
        print(f"missing env: {missing}", file=sys.stderr)
        return 2

    if not os.environ.get(BOOKS[args.book]):
        defaults = {
            "suryodaya": "https://agentswitch.theschoolofai.in",
            "keystone": "https://class.agentswitch.theschoolofai.in",
        }
        base = defaults[args.book]
    client = McpClient(base, email, password)
    agent = DirectoryAgent(client, apply_writes=args.apply_writes or os.environ.get("APPLY_WRITES") == "1")
    me = agent.connect()
    result = agent.handle(args.request)
    print(json.dumps({"me": {"email": me.get("email"), "allowed_apps": me.get("allowed_apps")}, "result": result}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
