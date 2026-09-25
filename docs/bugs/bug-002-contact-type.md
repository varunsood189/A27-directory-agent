# Bug 2 evidence — Keystone contact_type vs roles.customer

**Seat:** 27 Directory. **Book:** Keystone vs Suryodaya. **Company:** `c1e47d8d-b849-4187-9a32-4103d3dece4a`
**Date:** 2026-09-25
**Tool:** `Party.list`
**Severity:** High
**Report id:** `94be1601-6dd1-4ade-a01c-38317e39d9a1`

## Repro

```
Party.list {}                         # Keystone total=100, Suryodaya total=194
Party.list {contact_type: "customer"} # Keystone total=0,   Suryodaya total=44
Party.list {roles: "customer"}        # both: JSON-RPC -32602, roles is not an accepted argument
```

UI: Keystone All Contacts → All Customers still shows **11** rows (e.g. Allegheny Harvest Systems LLC `62f8d1c3-1fc9-4e16-b967-1463c2c86936`, `roles.customer`, `contact_type` null).

## Result

| | Suryodaya | Keystone |
|---|---|---|
| `Party.list` (no contact_type) | 194 | 100 |
| `contact_type=customer` | **44** | **0** |
| rows with `roles.customer` | 44 | **11** |
| `contact_type` null | 138 | **100** |

Schema enum for `contact_type`: `customer`, `vendor`, `both`. No `roles` filter on `Party.list`.

Expected: Keystone customers flagged like Suryodaya (`contact_type=customer` total matches `roles.customer`).

Not this bug: `currency_id=locale:base_currency` → 0 and `search=%` matching the whole book (team20; do not re-file).
