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

## Live counts (2026-09-18, MCP)

| | Suryodaya | Keystone |
|---|---|---|
| `Party.list` | 194 | 100 |
| `type=organization` | 16 | 18 |
| `contact_type=customer` | 44 | **0** — do not use this filter as “the customer list” |
| `PartyRelationship.list` | **0** | 28, mostly `represents` (person → org) |
| `AddressBook.list` | 8 | 3 |
| `ContactGroup.list` | 12 | 3 |

`Party` rows: `name` filled; `first_name` / `last_name` / `job_title` / `company_name` often null. `Party.delete` is not in `tools/list`. Dedup is update + relationship, not delete.

Re-checked **2026-09-22** (other teams changed data — this is the point of the shared book):

- **Ajay Bansode** `55df0b62-…` employee `ajay.bansode@suryodaya.in` vs **Ajay Iyer** `a84fb127-…` customer `ajay.iyer@yahoo.in`. Same first name, **not** a merge.
- Search `Angle Plate` now returns **0**. Those rows were renamed; e.g. old `Angle Plate 8886` / `anil.thorat8886@corp.in` is now **Anil Thorat**. `Party.list` `search` does not match substrings in the old SKU names.
- Real dupes on the list: **Aarti Deshpande** and **Aarti Deshpande (2)** (different emails `…8918@corp.in` vs `…8928@mail.in`). Same pattern for Patil, Bhosale (2 and 3), Pawar, Rane, Gaikwad — 8 ` (2)`/` (3)` rows, all prospects.
- Keystone **Hocking Hills Mower Works** `1a849375-…`: one `represents` edge, **Matt Swaim** `mswaim@hockinghillsmower.com`, VP Manufacturing.

Example Keystone who-we-know edge: Matt Swaim `represents` Hocking Hills Mower Works (`from_party_id` `92221acd-…`, `to_party_id` `1a849375-…`).

Suryodaya address book names look like inventory (`V-Block Pair 86mm (Box)`), `source=carddav_import`. MCP list works; the UI “complete record set could not be loaded” banner is still a candidate UI bug.

## Seat request vs these tools

| Goal | Orchestration |
|---|---|
| Deduplicate | Page `Party.list`, cluster email then name, re-get, `Party.update` and/or `PartyRelationship.create` (`associate`). No merge tool. No delete. |
| Who do we know | Keystone: `PartyRelationship.list` `represents`/`employee`/`employer`. Suryodaya: graph is empty — search / `company_name`, and refuse to invent edges. |

## Locale

`GET /api/accounting/locale` → 403 (`accounting` not enabled). Seat boundary. Do not report. Do not `PUT`.

## UI (Keystone)

Nav includes All Contacts, Suppliers, Contact Groups, Address Books, Drive.

Shell error seen: **“The complete record set could not be loaded. Refresh and try again; no partial total is shown.”** (near Address Books / contacts). Candidate UI bug — file only if you can still reproduce it on All Contacts or Address Books.

## Not done

- You: ten minutes on All Contacts (open a real party, look for duplicate names).
- You: open Attio (gap report already uses it).
- You: week-1 upload URL on Axiom.
- You: handwritten tests later (I do not write those files).
