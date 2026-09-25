# Gap report — Directory vs Attio

Seat 27 Directory Agent. Comparison: [Attio](https://attio.com) ([hosted MCP](https://docs.attio.com/mcp/overview)). Attio is the AI-native CRM analogue (merge, upsert, “who do we know at Stripe”). We are the contacts spine: `Party` / `PartyRelationship`.

Re-measured **2026-09-25**, team27. Suryodaya **194** parties (`contact_type=customer` **44** = `roles.customer` **44**), **0** relationships, eight `(2)`/`(3)` name dupes. Keystone **100** parties, **28** `represents` edges (Hocking Hills → Matt Swaim). Keystone `contact_type` is **null on all 100**; `Party.list contact_type=customer` total **0**; UI All Customers still shows **11** (`roles.customer`). Do not treat that filter as the customer list.

## 1. What they do that we do not

Competitor product, not our defects:

- **Merge as a primitive.** Attio MCP `merge-records`. We have `Party.update`. No `Party.delete`, no `Party.merge`.
- **Upsert on email/domain.** Attio `upsert-record`. `Party.create` will add a second row.
- **Who-we-know from mailbox/calendar.** Attio prices connection strength. `Party.email` is a field. Mail is another seat.
- **Enrichment.** Attio fills ARR, funding, socials. Our tax fields are rich; `first_name` / `job_title` are often empty.

## Filed / to-file defects (ours, not Attio features)

Do **not** re-file team20 Files/platform reports (filter defaults, `%`/`_` search, date-as-text, enum omit, scheduler, Drive revisions, `content_hash`, token counter, people-directory-lists-companies, …). Those are already on the class board.

| # | Bug | Book | Status |
|---|---|---|---|
| 1 | All Contacts banner **11 Active Customers** vs segment **Active (90d) = 0** and empty list | Keystone | Filed in-app 24 Sep. Paste the report id here when you have it. |
| 2 | `Party.list contact_type=customer` total **0**; all `contact_type` null; **11** rows have `roles.customer`; `roles` is **not** an accepted list filter. UI All Customers shows those 11. Suryodaya same filter returns 44. | Keystone | **File this.** Paste below. |
| — | `Party.merge` / `Party.delete` missing | both | Feature request only if you want a third report. Not a crash. |

Agent workarounds already in this repo: page all parties (do not send advertised `Party.list` defaults — `currency_id=locale:base_currency` returns 0, same class as team20 #1). Do not send `PartyRelationship.list relationship=associate` (advertised default; Keystone graph is all `represents`, total becomes 0). Do not filter Keystone customers on `contact_type`. Never call missing payroll tools.

## 2. Which gaps an agent can close with today’s tools

Graded goals: `directory.deduplicate_customers`, `directory.who_do_we_know` (empty official predicates — harness uses `Party.get` ids).

Closeable now: `Party.list` + `Party.get`; cluster on normalised name (strip ` (2)`); re-get before any write; `PartyRelationship.create` `associate` — never delete. On Keystone, `PartyRelationship.list` `from_party_id` / `to_party_id` (omit `relationship` unless you mean it). On Suryodaya, say the graph is empty. Refuse payroll. Do not pass extra args (`additionalProperties: false` is correct, not a bug).

Platform still: merge API, mailbox strength, enrichment, upsert-by-email, a `roles` filter on `Party.list`, `contact_type` populated on the US book.

## 3. What an agent can do that Attio’s product cannot

Hold the Section 8 sentence as one goal: walk 194 parties, name the `(2)` clusters, answer Hocking Hills (Matt Swaim) after a re-read, and refuse when Godrej has no relationship edges. Other teams already renamed “Angle Plate 8886” to Anil Thorat under us; a UI click from last week is stale. Their product will not notice.
