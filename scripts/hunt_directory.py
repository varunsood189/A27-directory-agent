"""Read-only Directory hunt. Prints compact findings. No writes. No secrets."""

from __future__ import annotations

import json
import os
import sys
from collections import Counter

sys.path.insert(0, ".")
from src.mcp_client import McpClient, McpError  # noqa: E402


def connect(book: str) -> McpClient:
    base = os.environ["AS_SURYODAYA" if book == "suryodaya" else "AS_KEYSTONE"]
    pw = os.environ["AS_PASSWORD_SURYODAYA" if book == "suryodaya" else "AS_PASSWORD_KEYSTONE"]
    c = McpClient(base, os.environ["AS_EMAIL"], pw, "team27-hunt")
    c.login()
    c.handshake()
    return c


def call(c: McpClient, tool: str, args: dict):
    try:
        r = c.call_tool(tool, args)
        return "ok", r
    except McpError as e:
        return "err", {"http": e.http_status, "msg": str(e)[:240], "payload": e.payload}


def total(payload):
    if isinstance(payload, dict):
        return payload.get("total"), len(payload.get("data") or [])
    return None, None


def schema_props(tools, name):
    for t in tools:
        if t.get("name") == name:
            schema = t.get("inputSchema") or t.get("input_schema") or {}
            return schema.get("properties") or {}, schema
    return {}, {}


def hunt(book: str) -> None:
    print(f"\n======== {book} ========", flush=True)
    c = connect(book)
    listed = c.rpc("tools/list")
    tools = listed.get("tools") if isinstance(listed, dict) else listed
    if isinstance(listed, dict) and not isinstance(tools, list):
        tools = (listed.get("structuredContent") or {}).get("tools") or []
    names = {t.get("name") for t in tools if isinstance(t, dict)}
    party_props, party_schema = schema_props(tools, "Party.list")
    rel_props, _ = schema_props(tools, "PartyRelationship.list")
    get_props, _ = schema_props(tools, "Party.get")

    print("Party.delete" in names, "Party.merge" in names, "tools.search" in names)

    cases = [
        ("list none", "Party.list", {"limit": 1}),
        ("list limit 0", "Party.list", {"limit": 0}),
        ("list limit -1", "Party.list", {"limit": -1}),
        ("list offset -1", "Party.list", {"offset": -1, "limit": 1}),
        ("list offset 10k", "Party.list", {"offset": 10000, "limit": 5}),
        ("list type individual", "Party.list", {"type": "individual", "limit": 1}),
        ("list type org", "Party.list", {"type": "organization", "limit": 1}),
        ("list contact both", "Party.list", {"contact_type": "both", "limit": 5}),
        ("list vendor", "Party.list", {"contact_type": "vendor", "limit": 5}),
        ("list sub_type business", "Party.list", {"customer_sub_type": "business", "limit": 5}),
        ("get missing uuid", "Party.get", {"id": "00000000-0000-0000-0000-000000000000"}),
        ("get not uuid", "Party.get", {"id": "not-a-uuid"}),
        ("rel none", "PartyRelationship.list", {"limit": 5}),
        ("rel associate", "PartyRelationship.list", {"relationship": "associate", "limit": 5}),
        ("rel represents", "PartyRelationship.list", {"relationship": "represents", "limit": 5}),
        ("rel employee", "PartyRelationship.list", {"relationship": "employee", "limit": 5}),
        ("rel is_active true", "PartyRelationship.list", {"is_active": True, "limit": 5}),
        ("rel is_active false", "PartyRelationship.list", {"is_active": False, "limit": 5}),
        ("rel is_primary true", "PartyRelationship.list", {"is_primary": True, "limit": 5}),
        ("books", "AddressBook.list", {"limit": 20}),
        ("entries", "AddressBookEntry.list", {"limit": 20}),
        ("groups", "ContactGroup.list", {"limit": 20}),
        ("members", "ContactGroupMember.list", {"limit": 20}),
        ("lead", "Lead.list", {"limit": 3}),
        ("deal", "Deal.list", {"limit": 3}),
        ("note", "Note.list", {"limit": 3}),
        ("activity", "Activity.list", {"limit": 3}),
        ("book get missing", "AddressBook.get", {"id": "00000000-0000-0000-0000-000000000000"}),
        ("group get missing", "ContactGroup.get", {"id": "00000000-0000-0000-0000-000000000000"}),
        ("rel get missing", "PartyRelationship.get", {"id": "00000000-0000-0000-0000-000000000000"}),
        ("sort bogus", "Party.list", {"sort_by": "not_a_field", "limit": 1}),
        ("search empty", "Party.list", {"search": "", "limit": 3}),
        ("search space", "Party.list", {"search": "   ", "limit": 3}),
        ("search email domain", "Party.list", {"search": "@suryodaya.in", "limit": 5}),
        ("first_name nullish", "Party.list", {"first_name": "null", "limit": 3}),
        ("company_name empty", "Party.list", {"company_name": "", "limit": 3}),
    ]
    for title, tool, args in cases:
        kind, payload = call(c, tool, args)
        if kind == "ok":
            t, n = total(payload)
            extra = ""
            if title in {"books", "groups"} and isinstance(payload, dict):
                extra = " names=" + str([r.get("name") for r in (payload.get("data") or [])][:8])
            print(f"  {title:28} ok total={t} n={n}{extra}")
        else:
            err = payload.get("payload") or {}
            code = None
            if isinstance(err, dict):
                code = (err.get("error") or {}).get("code") if "error" in err else err.get("code")
                if payload.get("http"):
                    code = f"http={payload['http']} rpc={code}"
            print(f"  {title:28} ERR {payload.get('msg')}")

    # Field completeness on first page of parties
    page = c.call_tool("Party.list", {"limit": 100, "offset": 0, "sort_by": "name", "sort_order": "asc"})
    rows = page.get("data") or []
    n = len(rows)
    print("  page0", n, "total", page.get("total"))
    print("  first_name empty", sum(1 for r in rows if not r.get("first_name")))
    print("  last_name empty", sum(1 for r in rows if not r.get("last_name")))
    print("  email empty", sum(1 for r in rows if not r.get("email")))
    print("  job_title empty", sum(1 for r in rows if not r.get("job_title")))
    print("  company_name empty", sum(1 for r in rows if not r.get("company_name")))
    print("  contact_type", dict(Counter(r.get("contact_type") for r in rows)))
    emails = [(r.get("email") or "").lower() for r in rows if r.get("email")]
    dups = [e for e, k in Counter(emails).items() if k > 1]
    print("  duplicate emails on page", dups[:8])

    # Party.get vs list row keys
    if rows:
        gid = rows[0]["id"]
        got = c.call_tool("Party.get", {"id": gid})
        list_keys = set(rows[0])
        get_keys = set(got) if isinstance(got, dict) else set()
        print("  get-only keys", sorted(get_keys - list_keys)[:20])
        print("  list-only keys", sorted(list_keys - get_keys)[:20])
        print("  get name", got.get("name") if isinstance(got, dict) else None, "list name", rows[0].get("name"))

    # Address book entries vs books
    books = c.call_tool("AddressBook.list", {"limit": 50})
    entries = c.call_tool("AddressBookEntry.list", {"limit": 50})
    groups = c.call_tool("ContactGroup.list", {"limit": 50})
    members = c.call_tool("ContactGroupMember.list", {"limit": 50})
    print("  books", books.get("total"), "entries", entries.get("total"), "groups", groups.get("total"), "members", members.get("total"))
    book_ids = {b.get("id") for b in books.get("data") or []}
    entry_books = Counter(e.get("address_book_id") or e.get("book_id") for e in entries.get("data") or [])
    print("  entry book keys sample", list((entries.get("data") or [{}])[0].keys())[:20] if entries.get("data") else None)
    print("  entry_books", dict(entry_books))
    if entries.get("data"):
        print("  entry0", json.dumps(entries["data"][0], default=str)[:500])
    if members.get("data"):
        print("  member0", json.dumps(members["data"][0], default=str)[:500])
    if groups.get("data"):
        print("  group names", [g.get("name") for g in groups.get("data")])

    # tools.search if present
    if "tools.search" in names:
        kind, payload = call(c, "tools.search", {"query": "Party"})
        print("  tools.search Party", kind, str(payload)[:300])

    print("  Party.list defaults in schema", {k: v.get("default") for k, v in party_props.items() if isinstance(v, dict) and "default" in v})
    print("  Rel defaults", {k: v.get("default") for k, v in rel_props.items() if isinstance(v, dict) and "default" in v})
    print("  Party.list additionalProperties", party_schema.get("additionalProperties"))


def main():
    hunt("suryodaya")
    hunt("keystone")


if __name__ == "__main__":
    main()
