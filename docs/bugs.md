# Directory bugs (seat 27)

Team27. File in-app via **Report a problem**. Do **not** re-file team20 #1–17 (filter defaults, `%`/`_` search, Drive, scheduler, token counter, **people directory lists companies**). Do not file 403 locale, extra-arg reject, or `GET /api/mcp` 405.

| # | Date | Book | Tool / screen | One line | Evidence | In-app id | Status |
|---|------|------|---------------|----------|----------|-----------|--------|
| 1 | 2026-09-24 | Keystone | All Contacts → Active (90d) | Banner **11 Active Customers**; sidebar **Active (90d) = 0**; list empty | [bug-001-active-customers.md](bugs/bug-001-active-customers.md) | *(paste id)* | filed |
| 2 | 2026-09-25 | Keystone | `Party.list` `contact_type=customer` | Filter total **0**; all 100 `contact_type` null; **11** `roles.customer`; `roles` not a list filter. Suryodaya same filter **44**. | [bug-002-contact-type.md](bugs/bug-002-contact-type.md) | `94be1601-6dd1-4ade-a01c-38317e39d9a1` | filed |

Bug 2 filed. In-app id `94be1601-6dd1-4ade-a01c-38317e39d9a1`. If you still have bug 1’s id, paste it in the table above.
