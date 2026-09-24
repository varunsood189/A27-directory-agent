# Gap report — Directory vs Attio

Seat 27 Directory Agent. Week 1. Comparison: [Attio](https://attio.com) ([pricing](https://attio.com/pricing), [hosted MCP](https://docs.attio.com/mcp/overview)). Same role Rillet plays for Ledger: AI-native CRM that already ships MCP (`merge-records`, `upsert-record`, “find all contacts at Stripe”).

Live book, team27, 2026-09-22: Suryodaya **194** parties, **0** `PartyRelationship` rows, named duplicates `Aarti Deshpande` / `Aarti Deshpande (2)` (and six similar `(2)`/`(3)` prospects). Keystone **100** parties, **28** relationships; **Hocking Hills Mower Works** → **Matt Swaim** (`represents`, VP Manufacturing). `contact_type=customer` is 44 vs **0** — that filter is not “the customer list” on the US book. UI on Keystone All Contacts (2026-09-24) lists those 11 customers; in-app report filed for the **11 Active Customers** banner vs **Active (90d)** empty/0.

## 1. What they do that we do not

- **Merge as a primitive.** Attio MCP `merge-records`. We have `Party.update`, no `Party.delete`, no merge tool.
- **Upsert on email/domain.** Attio `upsert-record`. `Party.create` will add a second row.
- **Who-we-know from mailbox/calendar.** Attio prices connection strength. Email is another seat; `Party.email` is a field, not a thread.
- **Enrichment.** Attio fills ARR, funding, socials. Our tax fields (GST / W9) are rich; `first_name` / `job_title` are often empty.
- **Search that means everyone at the company.** We orchestrate `Party.list` + `PartyRelationship.list`. On Suryodaya that graph is empty.

## 2. Which gaps an agent can close with today’s tools

Closeable now: page all parties; cluster on normalised name (strip ` (2)`); re-get before any write; link with `PartyRelationship` `associate` — never delete. On Keystone, list `represents` for the org. On Suryodaya, say the graph is empty. Refuse payroll (tools are absent). Do not filter `contact_type=customer` as the whole list.

Platform: merge API, mailbox strength, enrichment, upsert-by-email. Empty official predicates (`directory.deduplicate_customers`, `directory.who_do_we_know`) — our harness checks `Party.get` ids instead.

## 3. What an agent can do that Attio’s product cannot

Hold the Section 8 sentence as one goal: walk 194 parties, name the `(2)` clusters, then answer Hocking Hills (Matt Swaim) after a re-read, and refuse when Godrej has no relationship edges. Other teams already renamed “Angle Plate 8886” to Anil Thorat under us; a UI click from last week is stale. Their product will not notice.
