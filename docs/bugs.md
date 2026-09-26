# Bugs filed against AgentSwitch — Directory seat (Team 27)

All bugs filed via the platform's **Report a problem** form, with evidence committed to this repo.

Do **not** re-file team20 #1–17 or team17 Contracts reports. Do not file 403 locale, extra-arg reject, or `GET /api/mcp` 405. `tools.search` tagging Party as `core` is the same class as team20 #16 — skip.

| # | Date | Tool | Summary | Severity | Evidence | Report id |
|---|------|------|---------|----------|----------|-----------|
| 1 | 2026-09-24 | All Contacts → Active (90d) | Keystone banner **11 Active Customers**; sidebar **Active (90d) = 0**; list empty | Medium | [bug-001-active-customers.md](bugs/bug-001-active-customers.md) | not recovered |
| 2 | 2026-09-25 | `Party.list` | `contact_type=customer` total **0** on Keystone; 11 `roles.customer`; no `roles` filter. Suryodaya **44**. | High | [bug-002-contact-type.md](bugs/bug-002-contact-type.md) | `94be1601-6dd1-4ade-a01c-38317e39d9a1` |
| 3 | 2026-09-26 | `PartyRelationship.list` | Schema default `relationship=associate`. Sending it on Keystone returns **0**; omit it → **28** `represents`. Who-we-know graph disappears. | High | [bug-003-relationship-default.md](bugs/bug-003-relationship-default.md) | `a9a923b6-ce45-482f-8f8b-3aebabc9ee03` |
| 4 | 2026-09-26 | `Party.get` (also AddressBook/ContactGroup/PartyRelationship.get) | Missing id is `not_found` but JSON-RPC code is **-32602** (invalid params), not a not-found code. | Medium | [bug-004-not-found-code.md](bugs/bug-004-not-found-code.md) | `d8ec8e3e-a74a-4a6b-9b9b-e858983d1b15` |
| 5 | 2026-09-26 | `Party.get` | `id: "not-a-uuid"` returns **Party not found**, not invalid_arguments. | Medium | [bug-005-get-non-uuid.md](bugs/bug-005-get-non-uuid.md) | `05f734c2-420f-46bd-b134-fb8f9cb3ce73` |
| 6 | 2026-09-26 | Contact Groups | Groups named Investors / Newsletter / VIP Clients. All 6 members on both books are **organizations**, not people. | Medium | [bug-006-groups-are-orgs.md](bugs/bug-006-groups-are-orgs.md) | `5e2bf33f-6391-4c1c-a4d1-fe0ed321d80b` |
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

6 filed. **4 to-file** (7–10 on Suryodaya). 0 withdrawn. 0 duplicates.

## How these were found (not Ask Agent)

The in-app **Ask Agent** chat is **not assigned** to `team27@…` (`Your agent is not available to this login yet`). That is expected. **Do not use Ask Agent to reproduce.**

Bugs were measured with **MCP** `POST /api/mcp` (login as team27, same as the Directory agent in this repo): `scripts/hunt_directory.py`. Report a problem from the matching **UI screen**; paste the measured totals. Instructor scores MCP/API defects.

| # | Can you see it without agent? | Keep? |
|---|-------------------------------|-------|
| 1 | Yes — Keystone All Customers banner **11 Active Customers**, sidebar Active (90d) **0** | Filed. Do not re-file. |
| 2 | UI shows 11 customers; `contact_type=customer` **0** is MCP | Filed. |
| 3 | No UI control for `relationship=associate`. MCP only | **Filed** `a9a923b6-ce45-482f-8f8b-3aebabc9ee03` |
| 4 | MCP only (error code) | **Filed** `d8ec8e3e-a74a-4a6b-9b9b-e858983d1b15` |
| 5 | MCP only (bad id) | **Filed** `05f734c2-420f-46bd-b134-fb8f9cb3ce73` |
| 6 | Yes — Contact Groups | **Filed** `5e2bf33f-6391-4c1c-a4d1-fe0ed321d80b` |
| 7 | Yes — Suryodaya Contact Groups | Keep. |
| 8 | Yes — Suryodaya Address Books | Keep. |
| 9 | Yes — open a Suryodaya person; first/last empty. `sort_by=first_name` is MCP | Keep. |
| 10 | Yes — All Contacts search, type only spaces | Keep (low). |

**Not bugs on the screenshot you pasted:** yellow financial banner; **Showing 5 records** (you are on **Tier B**, which is 5); Ask Agent unassigned; ₹ credit limits while financial context is off (do not file as 403 locale). **Lapsed=11** / **New This Quarter=11** is the same family as bug 1 — do not file a second report.

## How to file 3–10

Stay on the screen in each paste. One report per row. Copy the block from the matching evidence file. No Ask Agent.

**Where to file:** bugs **1–6** on Keystone `https://class.agentswitch.theschoolofai.in`. Bugs **7–10** on Suryodaya `https://agentswitch.theschoolofai.in` (empty groups/books and first/last are India-book data). Do not file 7–10 on Keystone.
