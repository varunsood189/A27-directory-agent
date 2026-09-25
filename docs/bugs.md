# Bugs filed against AgentSwitch — Directory seat (Team 27)

All bugs filed via the platform's **Report a problem** form, with evidence committed to this repo.

Do **not** re-file team20 #1–17 (filter defaults, `%`/`_` search, Drive, scheduler, token counter, people directory lists companies). Do not file 403 locale, extra-arg reject, or `GET /api/mcp` 405.

| # | Date | Tool | Summary | Severity | Evidence | Report id |
|---|------|------|---------|----------|----------|-----------|
| 1 | 2026-09-24 | All Contacts → Active (90d) | Keystone banner **11 Active Customers**; sidebar **Active (90d) = 0**; list empty | Medium | [bug-001-active-customers.md](bugs/bug-001-active-customers.md) | not recovered |
| 2 | 2026-09-25 | `Party.list` | `contact_type=customer` total **0** on Keystone; all 100 `contact_type` null; **11** `roles.customer`; `roles` is not a list filter. Suryodaya same filter **44**. | High | [bug-002-contact-type.md](bugs/bug-002-contact-type.md) | `94be1601-6dd1-4ade-a01c-38317e39d9a1` |

## Pattern

`Party.list` advertises `contact_type` as the customer filter. On Suryodaya that field matches `roles.customer`. On Keystone the field is empty, the UI All Customers list is driven by `roles`, and MCP has no `roles` filter. The Directory graded request cannot list “the customer list” with the documented argument on the US book.

## Withdrawn / corrected

- None withdrawn. Bug 1 was filed 24 Sep; the in-app id was not copied at the time (do not re-file).
- Advertised `Party.list` defaults (`currency_id=locale:base_currency` → 0) and `search=%` matching the whole book were **not** filed: already on the class board (team20).

## Total

2 valid bugs filed. 0 withdrawn. 0 duplicates closed.
