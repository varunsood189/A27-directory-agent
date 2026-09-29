"""Load book URLs and passwords. `.env` on disk wins over a truncated bash export (`!` eaten)."""

from __future__ import annotations

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

DEFAULTS = {
    "AS_SURYODAYA": "https://agentswitch.theschoolofai.in",
    "AS_KEYSTONE": "https://class.agentswitch.theschoolofai.in",
    "AS_EMAIL": "team27@theschoolofai.in",
    "APPLY_WRITES": "0",
}

PASSWORD_KEYS = ("AS_PASSWORD_SURYODAYA", "AS_PASSWORD_KEYSTONE")


def parse_env_file(path: Path) -> dict[str, str]:
    out: dict[str, str] = {}
    if not path.is_file():
        return out
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "'\"":
            value = value[1:-1]
        out[key] = value
    return out


def get(key: str, default: str | None = None) -> str | None:
    file_vals = parse_env_file(ROOT / ".env")
    file_val = file_vals.get(key)
    env_val = os.environ.get(key)
    if key in PASSWORD_KEYS:
        # Bash history expansion turns juInHHtf6r3Et0g3!aA1 into 16 chars. Prefer the file.
        if file_val:
            if not env_val or len(env_val) < len(file_val):
                return file_val
        if env_val:
            return env_val
        return file_val or default
    return env_val or file_val or DEFAULTS.get(key, default)


def book_base(book: str) -> str:
    key = "AS_SURYODAYA" if book == "suryodaya" else "AS_KEYSTONE"
    value = get(key)
    if not value:
        raise SystemExit(f"missing {key}")
    return value


def book_password(book: str) -> str:
    key = "AS_PASSWORD_SURYODAYA" if book == "suryodaya" else "AS_PASSWORD_KEYSTONE"
    value = get(key)
    if not value:
        raise SystemExit(
            f"missing {key}. Put the full password in {ROOT / '.env'} (gitignored). "
            "Do not export it in bash — `!` is stripped and login 401s."
        )
    return value


def email() -> str:
    return get("AS_EMAIL") or DEFAULTS["AS_EMAIL"]


def apply_writes() -> bool:
    return get("APPLY_WRITES") == "1"
