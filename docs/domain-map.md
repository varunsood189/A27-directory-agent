# Team 27 domain map — Directory Agent

Measured 2026-09-18. Login `team27@theschoolofai.in` unchanged.
Staff correction the same day: seats **20 and 27 were printed the wrong way round** in the first brief. Group is now **A27**.

**Seat: 27 Directory Agent.** Contacts and the core spine.

Graded request:

> Deduplicate the customer list, and tell me who we know at this company.

Goals: `directory.deduplicate_customers`, `directory.who_do_we_know` (empty circles on the seat page — no DB predicate yet).

## Who the server says we are

| | Suryodaya | Keystone |
|---|---|---|
| URL | https://agentswitch.theschoolofai.in | https://class.agentswitch.theschoolofai.in |
| `GET /api/auth/me` | HTTP 200 | HTTP 200 |
| `allowed_apps` | `agent`, `crm` | `agent`, `crm` |
| `roles` | `user`, `agent_user`, `sales_viewer` | same |
| MCP `tools/list` | 189 tools | 189 tools |

Course guide on Keystone matches this seat: **Seat 27 · Directory Agent**, Contacts / Core.

## MCP handshake

- Protocol `2025-11-25`, POST only.
- `GET /api/mcp` → HTTP 405 (no SSE).
- `notifications/initialized` → HTTP 202.

## Directory tools on this login

| Entity | Tools |
|---|---|
| `Party` | list, get, create, update |
| `PartyRelationship` | list, get, create, update |
| `AddressBook` | list, get, create, update, delete |
| `AddressBookEntry` | list, get, create, update, delete |
| `ContactGroup` | list, get, create, update, delete |
| `ContactGroupMember` | list, get, create, update, delete |
| `Company` | list, get |
| `Lead` | list, get |
| `Deal` | list, get |
| `Note` | list, get |
| `Activity` | list, get |

Also present (not the Directory goals): `FileAttachment.*`, agent workspace, CRM extras.

## Live counts (re-measured 2026-09-25, MCP)

| | Suryodaya | Keystone |
|---|---|---|
| `Party.list` | 194 | 100 |
| `type=organization` | 16 | 18 |
| `contact_type=customer` | **44** (matches `roles.customer`) | **0** — all 100 `contact_type` null; **11** `roles.customer` |
| `Party.list` `roles` filter | rejected (`additionalProperties: false`) | same |
| `PartyRelationship.list` omitted filter | **0** | **28**, all `represents` |
| `PartyRelationship.list relationship=associate` (schema default) | 0 | **0** — do not send the advertised default |
| `AddressBook.list` | 8, real names | 3 (`Suppliers`, `Team`, `Personal`) |
| `ContactGroup.list` | 12 | 3 |
| `Party.delete` / `Party.merge` | absent | absent |

`Party.list` advertised defaults include `currency_id: locale:base_currency`. Sending that string returns **0** rows (same class as team20 bug 1 — do not re-file). `search: "%"` or `"_"` matches the whole book (team20 bug 2 — do not re-file).

`Party` rows: `name` filled; `first_name` / `last_name` / `job_title` / `company_name` often null. `Party.delete` is not in `tools/list`. Dedup is update + relationship, not delete.

Re-checked **2026-09-22** (other teams changed data — this is the point of the shared book):

- **Ajay Bansode** `55df0b62-…` employee `ajay.bansode@suryodaya.in` vs **Ajay Iyer** `a84fb127-…` customer `ajay.iyer@yahoo.in`. Same first name, **not** a merge.
- Search `Angle Plate` now returns **0**. Those rows were renamed; e.g. old `Angle Plate 8886` / `anil.thorat8886@corp.in` is now **Anil Thorat**. `Party.list` `search` does not match substrings in the old SKU names.
- Real dupes on the list: **Aarti Deshpande** and **Aarti Deshpande (2)** (different emails `…8918@corp.in` vs `…8928@mail.in`). Same pattern for Patil, Bhosale (2 and 3), Pawar, Rane, Gaikwad — 8 ` (2)`/` (3)` rows, all prospects.
- Keystone **Hocking Hills Mower Works** `1a849375-…`: one `represents` edge, **Matt Swaim** `mswaim@hockinghillsmower.com`, VP Manufacturing.

Example Keystone who-we-know edge: Matt Swaim `represents` Hocking Hills Mower Works (`from_party_id` `92221acd-…`, `to_party_id` `1a849375-…`).

Suryodaya address book names were SKU-like on 2026-09-18 (`V-Block Pair 86mm (Box)`, `source=carddav_import`). Re-checked **2026-09-24**: All Contacts and Address Books load; book names are real (e.g. Suppliers — Purchasing). Do not file the old “complete record set could not be loaded” banner unless it comes back.

## Seat request vs these tools

| Goal | Orchestration |
|---|---|
| Deduplicate | Page `Party.list`, cluster email then name, re-get, `Party.update` and/or `PartyRelationship.create` (`associate`). No merge tool. No delete. |
| Who do we know | Keystone: `PartyRelationship.list` by `from_party_id` / `to_party_id` only (omit advertised `relationship=associate`). Suryodaya: graph is empty — do not invent edges. |

## Locale

`GET /api/accounting/locale` → 403 (`accounting` not enabled). Seat boundary. Do not report. Do not `PUT`.

## UI (Keystone, 2026-09-24)

Nav: All Contacts, Suppliers, Contact Groups, Address Books, Drive. All Contacts and Address Books load. There is no field labelled `contact_type`.

All Contacts → **All Customers** shows **11** records (Allegheny Harvest Systems LLC, Buckeye AgriPower, people with `roles=customer`, …). Every card says **No activity**. YTD / Outstanding are dashes.

**Ledger:** [`docs/bugs.md`](bugs.md). Bugs 1–6 filed (ids in bugs.md). 7–10 still Suryodaya.

Do not file: yellow “Financial context is not available” bar (no accounting locale, 403). Do not file 403 locale, missing payroll tools, extra-arg reject, `GET /api/mcp` 405. Do not re-file team20’s Files/platform reports (`%` search, advertised list defaults, people directory lists companies, scheduler, Drive, …).

## Not done

- You: handwritten pytest from `docs/test-spec.md` (I do not write those files).
- You: paste the GitHub URL when the teacher posts the harness submit link.
