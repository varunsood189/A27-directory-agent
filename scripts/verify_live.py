"""Read-only live checks. Not pytest (those you type yourself; generated tests score 0)."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.directory_agent import DirectoryAgent, is_refusal_request, normalize_name, party_list_args
from src.mcp_client import McpClient, McpError
from src import settings

PASS = 0
FAIL = 0
ROWS: list[str] = []


def check(name: str, ok: bool, detail: str = "") -> None:
    global PASS, FAIL
    if ok:
        PASS += 1
        ROWS.append(f"PASS  {name}" + (f"  {detail}" if detail else ""))
    else:
        FAIL += 1
        ROWS.append(f"FAIL  {name}" + (f"  {detail}" if detail else ""))


def connect(book: str) -> tuple[McpClient, DirectoryAgent]:
    client = McpClient(settings.book_base(book), settings.email(), settings.book_password(book), "team27-verify")
    agent = DirectoryAgent(client, apply_writes=False)
    agent.connect()
    return client, agent


def main() -> int:
    check("password keystone len 20", len(settings.book_password("keystone")) == 20, str(len(settings.book_password("keystone"))))
    check("password suryodaya len 20", len(settings.book_password("suryodaya")) == 20, str(len(settings.book_password("suryodaya"))))
    check("writes off", settings.apply_writes() is False)
    check("normalize (2)", normalize_name("Aarti Deshpande (2)") == "aarti deshpande")
    check("normalize spaces", normalize_name("  Matt   Swaim ") == "matt swaim")
    check("refuse payroll words", is_refusal_request("Show me the payroll and salary slips."))
    check("refuse invoice", is_refusal_request("open this invoice"))
    check("not refuse who", not is_refusal_request("Who do we know at Hocking Hills Mower Works?"))
    try:
        party_list_args({"contact_type": "customer"})
        check("blocked contact_type", False, "should raise")
    except ValueError:
        check("blocked contact_type", True)

    k, ak = connect("keystone")
    me = k.me()
    check("keystone login", me.get("email") == "team27@theschoolofai.in")
    check("allowed crm", "crm" in (me.get("allowed_apps") or []))

    listed = k.call_tool("Party.list", {"limit": 1})
    check("keystone parties > 0", int(listed.get("total") or 0) > 0, str(listed.get("total")))

    ct = k.call_tool("Party.list", {"contact_type": "customer", "limit": 1})
    check("keystone contact_type=customer is 0", int(ct.get("total") or 0) == 0, str(ct.get("total")))

    rel_all = k.call_tool("PartyRelationship.list", {"limit": 5})
    rel_as = k.call_tool("PartyRelationship.list", {"relationship": "associate", "limit": 5})
    rel_re = k.call_tool("PartyRelationship.list", {"relationship": "represents", "limit": 5})
    check("rel omit filter > 0", int(rel_all.get("total") or 0) > 0, str(rel_all.get("total")))
    check("rel associate 0", int(rel_as.get("total") or 0) == 0, str(rel_as.get("total")))
    check("rel represents > 0", int(rel_re.get("total") or 0) > 0, str(rel_re.get("total")))

    who = ak.handle("Who do we know at Hocking Hills Mower Works?")
    names = {normalize_name(p.get("name")) for p in (who.get("who") or [])}
    check("who not refused", who.get("refused") is False)
    check("who has Matt Swaim", "matt swaim" in names, str(sorted(names)))

    who_dot = ak.handle("Who do we know at Hocking Hills Mower Works.")
    check("who trailing period", "matt swaim" in {normalize_name(p.get("name")) for p in (who_dot.get("who") or [])})

    refuse = ak.handle("Show me the payroll and salary slips.")
    tools = [c.get("tool") or "" for c in k.calls]
    check("refuse true", refuse.get("refused") is True)
    check("refuse no salary tool", not any("SalarySlip" in t or "Payroll" in t for t in tools))

    try:
        k.call_tool("Party.list", {"limit": 1, "not_a_real_field": True})
        check("extra arg rejected", False, "call succeeded")
    except McpError as exc:
        check("extra arg rejected", "32602" in str(exc) or "invalid" in str(exc).lower(), str(exc)[:80])

    try:
        k.call_tool("Party.get", {"id": "not-a-uuid"})
        check("get non-uuid errors", False)
    except McpError:
        check("get non-uuid errors", True)

    s, as_ = connect("suryodaya")
    me_s = s.me()
    check("suryodaya login", me_s.get("email") == "team27@theschoolofai.in")
    dup = as_.handle("Deduplicate the customer list.")
    clusters = dup.get("clusters") or []
    check("dedupe clusters >= 1", len(clusters) >= 1, str(len(clusters)))
    check("dedupe links empty", all(not c.get("links") for c in clusters))
    two = any("(2)" in (m.get("name") or "") for c in clusters for m in (c.get("members") or []))
    check("dedupe has (2) name", two)

    empty = as_.handle("Who do we know at Godrej Material Handling?")
    check("godrej no invented who", not (empty.get("who") or []))
    check("godrej not refused", empty.get("refused") is False)

    print("\n".join(ROWS))
    print(f"\n{PASS} passed, {FAIL} failed, {PASS + FAIL} total")
    return 1 if FAIL else 0


if __name__ == "__main__":
    raise SystemExit(main())
