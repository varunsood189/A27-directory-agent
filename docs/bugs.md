# Bugs filed against AgentSwitch — Directory seat (Team 27)

All bugs filed via the platform's **Report a problem** form, with evidence committed to this repo.

Do **not** re-file team20 #1–17 or team17 Contracts reports. Do not file 403 locale, extra-arg reject, or `GET /api/mcp` 405. `tools.search` tagging Party as `core` is the same class as team20 #16 — skip.

| # | Date | Tool | Summary | Severity | Evidence | Report id |
|---|------|------|---------|----------|----------|-----------|
| 1 | 2026-09-24 | All Contacts → Active (90d) | Keystone banner **11 Active Customers**; sidebar **Active (90d) = 0**; list empty | Medium | [bug-001-active-customers.md](bugs/bug-001-active-customers.md) | not recovered |
| 2 | 2026-09-25 | `Party.list` | `contact_type=customer` total **0** on Keystone; 11 `roles.customer`; no `roles` filter. Suryodaya **44**. | High | [bug-002-contact-type.md](bugs/bug-002-contact-type.md) | `94be1601-6dd1-4ade-a01c-38317e39d9a1` |
| 3 | 2026-09-26 | `PartyRelationship.list` | Schema default `relationship=associate`. Sending it on Keystone returns **0**; omit it → **28** `represents`. Who-we-know graph disappears. | High | [bug-003-relationship-default.md](bugs/bug-003-relationship-default.md) | to-file |
| 4 | 2026-09-26 | `Party.get` (also AddressBook/ContactGroup/PartyRelationship.get) | Missing id is `not_found` but JSON-RPC code is **-32602** (invalid params), not a not-found code. | Medium | [bug-004-not-found-code.md](bugs/bug-004-not-found-code.md) | to-file |
| 5 | 2026-09-26 | `Party.get` | `id: "not-a-uuid"` returns **Party not found**, not invalid_arguments. | Medium | [bug-005-get-non-uuid.md](bugs/bug-005-get-non-uuid.md) | to-file |
| 6 | 2026-09-26 | Contact Groups | Groups named Investors / Newsletter / VIP Clients. All 6 members on both books are **organizations**, not people. | Medium | [bug-006-groups-are-orgs.md](bugs/bug-006-groups-are-orgs.md) | to-file |
| 7 | 2026-09-26 | `ContactGroup.list` | Suryodaya: **9 of 12** groups have **0** members (departmental names). All 6 members sit in Investors/Newsletter/VIP. | Medium | [bug-007-empty-groups.md](bugs/bug-007-empty-groups.md) | to-file |
| 8 | 2026-09-26 | `AddressBook.list` | Suryodaya: **5 of 8** books have **0** entries (`Suppliers — Purchasing`, …). All 8 entries sit in Suppliers/Team/Personal. | Medium | [bug-008-empty-address-books.md](bugs/bug-008-empty-address-books.md) | to-file |
| 9 | 2026-09-26 | `Party.list` / Party record | Suryodaya: `first_name` and `last_name` null on the listed individuals; `sort_by=first_name` returns **organizations**. `name` is filled. | High | [bug-009-empty-first-last.md](bugs/bug-009-empty-first-last.md) | to-file |
| 10 | 2026-09-26 | `Party.list` search | `search: ""` → total 194. `search: "   "` (spaces) → total **0**. | Low | [bug-010-search-whitespace.md](bugs/bug-010-search-whitespace.md) | to-file |

## Pattern

Directory customer/who-we-know tools disagree with their own schema: `contact_type` and `relationship` defaults/filters hide the live graph on Keystone; Suryodaya still has empty split-name fields and leftover empty groups/books.

## Withdrawn / corrected

- Bug 1 id not recovered; do not re-file.
- Not filed: advertised `Party.list` `currency_id=locale:base_currency` → 0, and `search=%` (team20).
- Not filed: `tools.search` `module=core` on Party (team20 #16 class).

## Total

2 filed. **8 to-file** (this hunt). 0 withdrawn. 0 duplicates.

## How to file 3–10

Stay on the screen in each paste. One report per row. Copy the block from the matching evidence file.
