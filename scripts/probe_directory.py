"""Read-only Directory probes. Prints findings. Never writes parties. Never prints secrets."""

from __future__ import annotations

import json
import os
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.mcp_client import McpClient, McpError  # noqa: E402

DIR_TOOLS = (
    "Party.list",
    "Party.get",
    "Party.create",
    "Party.update",
    "PartyRelationship.list",
    "AddressBook.list",
    "AddressBookEntry.list",
    "ContactGroup.list",
    "ContactGroupMember.list",
    "Company.list",
    "Lead.list",
    "Deal.list",
)


def schema_for(tools: list, name: str) -> dict:
    for t in tools:
        if t.get("name") == name:
            return t
    return {}


def compact_schema(tool: dict) -> dict:
    schema = (tool.get("inputSchema") or tool.get("input_schema") or {}) if tool else {}
    props = schema.get("properties") or {}
    out = {}
    for key, spec in props.items():
        if not isinstance(spec, dict):
            out[key] = spec
            continue
        row = {k: spec[k] for k in ("type", "default", "enum", "description") if k in spec}
        if "items" in spec:
            row["items"] = spec["items"]
        out[key] = row
    return {"required": schema.get("required"), "additionalProperties": schema.get("additionalProperties"), "properties": out}


def role_set(party: dict) -> set[str]:
    roles = party.get("roles") or []
    names = set()
    for item in roles:
        if isinstance(item, dict) and item.get("role"):
            names.add(str(item["role"]))
        elif isinstance(item, str):
            names.add(item)
    return names


def probe_book(label: str, base: str, email: str, password: str) -> dict:
    client = McpClient(base, email, password, client_name="team27-directory-probe")
    client.login()
    me = client.me()
    client.handshake()
    tools_payload = client.rpc("tools/list")
    tools = tools_payload.get("tools") if isinstance(tools_payload, dict) else tools_payload
    if isinstance(tools_payload, dict) and "structuredContent" in tools_payload:
        tools = (tools_payload.get("structuredContent") or {}).get("tools") or tools
    if not isinstance(tools, list):
        tools = []
    names = sorted(t.get("name") for t in tools if isinstance(t, dict))

    findings: list[str] = []
    schemas = {n: compact_schema(schema_for(tools, n)) for n in DIR_TOOLS}

    parties = client.list_all("Party.list", {"sort_by": "name", "sort_order": "asc"})
    rels = client.list_all("PartyRelationship.list")
    books = client.list_all("AddressBook.list")
    entries = client.list_all("AddressBookEntry.list")
    groups = client.list_all("ContactGroup.list")
    members = client.list_all("ContactGroupMember.list")

    type_counts = Counter(p.get("type") for p in parties)
    contact_type_counts = Counter(p.get("contact_type") for p in parties)
    role_counts = Counter()
    for p in parties:
        for r in role_set(p):
            role_counts[r] += 1

    customers_by_type = [p for p in parties if p.get("contact_type") == "customer"]
    customers_by_role = [p for p in parties if "customer" in role_set(p)]
    empty_name_parts = [
        p
        for p in parties
        if p.get("type") == "individual" and not (p.get("first_name") or p.get("last_name")) and p.get("name")
    ]
    dup_names = Counter((p.get("name") or "").strip() for p in parties)
    named_dupes = {k: v for k, v in dup_names.items() if k and v > 1}
    suffix_dupes = [p.get("name") for p in parties if p.get("name") and " (" in p.get("name") and p.get("name").rstrip().endswith(")")]

    rel_kinds = Counter(r.get("relationship") for r in rels)

    listed = client.call_tool("Party.list", {"contact_type": "customer", "limit": 5})
    listed_total = listed.get("total") if isinstance(listed, dict) else None

    default_probe = None
    props = (schemas.get("Party.list") or {}).get("properties") or {}
    advertised_defaults = {k: v.get("default") for k, v in props.items() if isinstance(v, dict) and "default" in v}
    if advertised_defaults:
        try:
            with_defaults = client.call_tool("Party.list", {k: v for k, v in advertised_defaults.items() if v is not None})
            default_probe = {
                "advertised": advertised_defaults,
                "total_when_sent": with_defaults.get("total") if isinstance(with_defaults, dict) else None,
                "total_omitted": len(parties),
            }
            if default_probe["total_when_sent"] not in (None, default_probe["total_omitted"]) and default_probe["total_when_sent"] == 0:
                findings.append("FILTER_DEFAULTS: sending advertised Party.list defaults returns 0 (same class as team20 bug 1 — do not re-file)")
        except McpError as exc:
            default_probe = {"advertised": advertised_defaults, "error": str(exc)}

    search_pct = client.call_tool("Party.list", {"search": "%", "limit": 5})
    search_us = client.call_tool("Party.list", {"search": "_", "limit": 5})
    search_pct_total = search_pct.get("total") if isinstance(search_pct, dict) else None
    search_us_total = search_us.get("total") if isinstance(search_us, dict) else None
    if (search_pct_total or 0) > 1 or (search_us_total or 0) > 1:
        findings.append("SEARCH_WILDCARD: Party.list search % or _ matches many rows (same class as team20 bug 2 — do not re-file)")

    bad_enum = None
    try:
        bad = client.call_tool("Party.list", {"contact_type": "not_a_real_type", "limit": 5})
        bad_enum = {"total": bad.get("total") if isinstance(bad, dict) else None, "error": None}
        if bad_enum["total"] == 0:
            findings.append("BAD_ENUM_ZERO: Party.list contact_type=not_a_real_type returns total=0 not 400 (same class as team20 bug 5 — do not re-file)")
    except McpError as exc:
        bad_enum = {"error": str(exc)}

    date_only = None
    if "created_at" in props or "updated_at" in props:
        field = "created_at" if "created_at" in props else "updated_at"
        try:
            date_only = client.call_tool("Party.list", {field: "2026-09-16", "limit": 5})
            date_only = {"field": field, "total": date_only.get("total") if isinstance(date_only, dict) else None}
        except McpError as exc:
            date_only = {"field": field, "error": str(exc)}

    enum_contact = None
    ct_spec = props.get("contact_type") if isinstance(props.get("contact_type"), dict) else {}
    if ct_spec.get("enum"):
        written = set(contact_type_counts) - {None}
        advertised = set(ct_spec["enum"])
        extra = written - advertised
        if extra:
            findings.append(f"ENUM_OMIT: Party.contact_type written {sorted(extra)} not in schema enum {sorted(advertised)} (same class as team20 bug 9 — do not re-file as generic)")
        enum_contact = {"schema": ct_spec["enum"], "written": dict(contact_type_counts)}

    if listed_total == 0 and customers_by_role:
        findings.append(
            f"DIRECTORY: contact_type=customer total={listed_total} but roles.customer={len(customers_by_role)} (FILE — Keystone customer list)"
        )
    if label == "suryodaya" and len(customers_by_type) != len(customers_by_role):
        findings.append(
            f"DIRECTORY: Suryodaya contact_type customers={len(customers_by_type)} vs roles.customer={len(customers_by_role)}"
        )

    rel_enum = ((schemas.get("PartyRelationship.list") or {}).get("properties") or {}).get("relationship") or {}
    if isinstance(rel_enum, dict) and rel_enum.get("enum"):
        extra_rel = set(rel_kinds) - {None} - set(rel_enum["enum"])
        if extra_rel:
            findings.append(f"ENUM_OMIT relationship written {sorted(extra_rel)} not in {rel_enum['enum']} (team20 class 9)")

    companies = client.call_tool("Company.list", {"limit": 20})
    orgs = [p for p in parties if p.get("type") == "organization"]
    company_rows = companies.get("data") if isinstance(companies, dict) else []

    computed_filters = []
    for key, spec in props.items():
        desc = str((spec or {}).get("description") or "").lower()
        if "comput" in desc or key in {"full_name", "display_name", "is_customer", "customer"}:
            computed_filters.append(key)
    if computed_filters:
        findings.append(f"COMPUTED_FILTERS on Party.list: {computed_filters} (same class as team20 bug 13 — do not re-file unless Directory-specific)")

    book_names = [b.get("name") for b in books]
    sku_like = [n for n in book_names if n and any(ch.isdigit() for ch in n) and ("mm" in n.lower() or "box" in n.lower())]

    return {
        "book": label,
        "me": {"email": me.get("email"), "roles": me.get("roles"), "allowed_apps": me.get("allowed_apps"), "company_id": me.get("company_id")},
        "tool_count": len(names),
        "has_party_delete": "Party.delete" in names,
        "has_party_merge": "Party.merge" in names,
        "schemas": schemas,
        "counts": {
            "parties": len(parties),
            "types": dict(type_counts),
            "contact_type": {str(k): v for k, v in contact_type_counts.items()},
            "roles": dict(role_counts),
            "contact_type_customer_filter_total": listed_total,
            "roles_customer": len(customers_by_role),
            "contact_type_customer_rows": len(customers_by_type),
            "relationships": len(rels),
            "relationship_kinds": dict(rel_kinds),
            "address_books": len(books),
            "address_book_entries": len(entries),
            "contact_groups": len(groups),
            "contact_group_members": len(members),
            "company_rows": len(company_rows or []),
            "party_orgs": len(orgs),
            "individuals_missing_first_last": len(empty_name_parts),
            "exact_duplicate_names": named_dupes,
            "suffix_dupes": suffix_dupes[:20],
            "address_book_names": book_names,
            "sku_like_books": sku_like,
        },
        "probes": {
            "advertised_defaults": advertised_defaults,
            "default_probe": default_probe,
            "search_pct_total": search_pct_total,
            "search_underscore_total": search_us_total,
            "bad_enum": bad_enum,
            "date_only": date_only,
            "enum_contact": enum_contact,
        },
        "findings": findings,
        "sample_role_customer": [
            {"id": p.get("id"), "name": p.get("name"), "type": p.get("type"), "contact_type": p.get("contact_type"), "roles": p.get("roles")}
            for p in customers_by_role[:8]
        ],
    }


def main() -> None:
    email = os.environ["AS_EMAIL"]
    out = {}
    for label, base_key, pw_key in (
        ("suryodaya", "AS_SURYODAYA", "AS_PASSWORD_SURYODAYA"),
        ("keystone", "AS_KEYSTONE", "AS_PASSWORD_KEYSTONE"),
    ):
        print(f"== {label} ==", flush=True)
        out[label] = probe_book(label, os.environ[base_key], email, os.environ[pw_key])
        for line in out[label]["findings"]:
            print(" ", line)
        c = out[label]["counts"]
        print("  parties", c["parties"], "ct_filter", c["contact_type_customer_filter_total"], "roles.customer", c["roles_customer"])
        print("  contact_type", c["contact_type"], "roles", c["roles"])
        print("  rels", c["relationships"], "books", c["address_books"], c["address_book_names"])
        print("  schema defaults Party.list", out[label]["probes"]["advertised_defaults"])
        print("  search %", out[label]["probes"]["search_pct_total"], "_", out[label]["probes"]["search_underscore_total"])
        print("  bad_enum", out[label]["probes"]["bad_enum"], "date", out[label]["probes"]["date_only"])
        print("  delete/merge", out[label]["has_party_delete"], out[label]["has_party_merge"])
        print("  sample customers", json.dumps(out[label]["sample_role_customer"], default=str)[:1500])
        print(flush=True)

    dest = ROOT / "docs" / "live" / "probe_directory.json"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(out, indent=2, default=str)[:400000])
    print("wrote", dest)


if __name__ == "__main__":
    try:
        main()
    except KeyError as e:
        print(f"missing env {e}", file=sys.stderr)
        sys.exit(2)
