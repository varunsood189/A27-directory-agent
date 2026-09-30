#!/usr/bin/env python3
"""Run the Directory agent against one book."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.directory_agent import DirectoryAgent
from src.mcp_client import McpClient, McpError
from src import settings

DEFAULT_REQUEST = "Deduplicate the customer list, and tell me who we know at this company."

BOOKS = ("suryodaya", "keystone")


def main() -> int:
    """CLI: --book suryodaya|keystone, --request text. Prints me + agent JSON. Returns 0 on success."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--book", choices=BOOKS, default="suryodaya")
    parser.add_argument("--request", default=DEFAULT_REQUEST)
    parser.add_argument("--apply-writes", action="store_true")
    args = parser.parse_args()

    try:
        base = settings.book_base(args.book)
        password = settings.book_password(args.book)
        email = settings.email()
    except SystemExit as exc:
        print(exc, file=sys.stderr)
        return 2
    client = McpClient(base, email, password)
    agent = DirectoryAgent(client, apply_writes=args.apply_writes or settings.apply_writes())
    try:
        me = agent.connect()
    except McpError as exc:
        if exc.http_status == 401:
            print(
                f"login 401: book={args.book} url={base} email={email} password_len={len(password)}. "
                "Put the full password in .env (gitignored). A 16-char bash export is truncated.",
                file=sys.stderr,
            )
        raise
    result = agent.handle(args.request)
    print(json.dumps({"me": {"email": me.get("email"), "allowed_apps": me.get("allowed_apps")}, "result": result}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
