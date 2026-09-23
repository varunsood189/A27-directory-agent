"""Directory agent: dedupe parties and list who we know at a company. MCP only."""

from __future__ import annotations

import re
import unicodedata
from collections import defaultdict
from typing import Any

from src.mcp_client import McpClient, McpError

REFUSE_MARKERS = (
    "salary",
    "payroll",
    "payslip",
    "salaryslip",
    "invoice",
    "work order",
    "workorder",
    "gst return",
)

SUFFIX = re.compile(r"\s*\(\d+\)\s*$")


def normalize_name(name: str | None) -> str:
    text = unicodedata.normalize("NFKC", name or "")
    text = SUFFIX.sub("", text)
    return " ".join(text.lower().split())


def is_refusal_request(request: str) -> bool:
    lowered = request.lower()
    return any(m in lowered for m in REFUSE_MARKERS)


def extract_company(request: str) -> str | None:
    patterns = [
        r"who do we know at\s+(.+?)\??$",
        r"at this company[:\s]+(.+?)\??$",
        r"at\s+(.+?)\??$",
    ]
    lowered = request.strip()
    for pat in patterns:
        match = re.search(pat, lowered, re.I)
        if match:
            name = match.group(1).strip().strip('"').strip("'")
            name = re.sub(r"^the\s+", "", name, flags=re.I)
            name = name.rstrip("?.!,;:")
            if name.lower() in {"this company", "that company", "the company"}:
                return None
            if name and "customer list" not in name.lower():
                return name
    return None


class DirectoryAgent:
    def __init__(self, client: McpClient, apply_writes: bool = False):
        self.client = client
        self.apply_writes = apply_writes

    def connect(self) -> dict[str, Any]:
        self.client.login()
        me = self.client.me()
        self.client.handshake()
        return me

    def handle(self, request: str) -> dict[str, Any]:
        if is_refusal_request(request):
            return {
                "refused": True,
                "reason": "This seat cannot read payroll, invoices, or other apps. Escalate to an EA, admin, or the owning team. Missing tools are not called.",
                "clusters": [],
                "who": [],
                "company": None,
            }

        want_dedupe = "dedup" in request.lower() or "duplicate" in request.lower() or "customer list" in request.lower()
        company = extract_company(request)
        want_who = "who do we know" in request.lower() or bool(company)

        if not want_dedupe and not want_who:
            want_dedupe = True
            want_who = True

        out: dict[str, Any] = {
            "refused": False,
            "reason": None,
            "clusters": [],
            "who": [],
            "company": company,
            "notes": [],
        }

        if want_dedupe:
            out["clusters"] = self.deduplicate()
        if want_who:
            who, note = self.who_at(company)
            out["who"] = who
            if note:
                out["notes"].append(note)
                if not who:
                    out["graph_empty"] = True
        return out

    def deduplicate(self) -> list[dict[str, Any]]:
        parties = self.client.list_all("Party.list", {"sort_by": "name", "sort_order": "asc"})
        buckets: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for party in parties:
            key = normalize_name(party.get("name"))
            if len(key) < 3:
                continue
            buckets[key].append(party)

        clusters = []
        for key, members in sorted(buckets.items()):
            if len(members) < 2:
                continue
            emails = {(m.get("email") or "").lower() for m in members}
            if len(emails) == 1 and all(emails):
                kind = "same_email"
            else:
                kind = "same_base_name"
            ids = [m["id"] for m in members if m.get("id")]
            for pid in ids:
                self.client.call_tool("Party.get", {"id": pid})
            linked = []
            if self.apply_writes and len(ids) >= 2:
                linked = self._link_associates(ids)
            clusters.append(
                {
                    "key": key,
                    "kind": kind,
                    "member_ids": ids,
                    "members": [
                        {
                            "id": m.get("id"),
                            "name": m.get("name"),
                            "email": m.get("email"),
                            "roles": m.get("roles"),
                        }
                        for m in members
                    ],
                    "links": linked,
                }
            )
        return clusters

    def _link_associates(self, ids: list[str]) -> list[dict[str, Any]]:
        created = []
        primary = ids[0]
        for other in ids[1:]:
            self.client.call_tool("Party.get", {"id": primary})
            self.client.call_tool("Party.get", {"id": other})
            try:
                row = self.client.call_tool(
                    "PartyRelationship.create",
                    {
                        "from_party_id": primary,
                        "to_party_id": other,
                        "relationship": "associate",
                        "notes": "team27 directory dedupe candidate — not a merge",
                    },
                )
                created.append({"id": (row or {}).get("id"), "from": primary, "to": other})
            except McpError as exc:
                created.append({"error": str(exc), "from": primary, "to": other})
        return created

    def who_at(self, company: str | None) -> tuple[list[dict[str, Any]], str | None]:
        if not company:
            return [], "No company name in the request."

        hits = self.client.call_tool("Party.list", {"search": company, "limit": 50})
        orgs = [p for p in (hits.get("data") or []) if isinstance(p, dict)]
        org = next((p for p in orgs if p.get("type") == "organization"), None)
        if org is None:
            org = next((p for p in orgs if normalize_name(p.get("name")) == normalize_name(company)), None)
        if org is None and orgs:
            org = orgs[0]
        if org is None:
            return [], f"No party matched {company!r}. Not inventing people."

        org_id = org["id"]
        self.client.call_tool("Party.get", {"id": org_id})
        people: dict[str, dict[str, Any]] = {}

        for filt in ({"to_party_id": org_id}, {"from_party_id": org_id}):
            rels = self.client.call_tool("PartyRelationship.list", {**filt, "limit": 100})
            for rel in rels.get("data") or []:
                if not isinstance(rel, dict):
                    continue
                other_id = rel["from_party_id"] if rel.get("to_party_id") == org_id else rel.get("to_party_id")
                if not other_id or other_id == org_id:
                    continue
                person = self.client.call_tool("Party.get", {"id": other_id})
                people[other_id] = {
                    "id": other_id,
                    "name": person.get("name") or rel.get("_from_party_id_display") or rel.get("_to_party_id_display"),
                    "email": person.get("email"),
                    "job_title": person.get("job_title"),
                    "relationship": rel.get("relationship"),
                    "notes": rel.get("notes"),
                    "org_id": org_id,
                    "org_name": org.get("name"),
                }

        if not people:
            fallback = self.client.call_tool("Party.list", {"search": org.get("name") or company, "limit": 50})
            for party in fallback.get("data") or []:
                if party.get("id") == org_id:
                    continue
                if normalize_name(party.get("company_name")) == normalize_name(org.get("name")):
                    people[party["id"]] = {
                        "id": party["id"],
                        "name": party.get("name"),
                        "email": party.get("email"),
                        "job_title": party.get("job_title"),
                        "relationship": None,
                        "notes": "matched company_name only; no PartyRelationship row",
                        "org_id": org_id,
                        "org_name": org.get("name"),
                    }

        if not people:
            return [], (
                f"Found org {org.get('name')} ({org_id}) but no relationship or company_name edges. "
                "Not inventing a contact."
            )
        return list(people.values()), None
