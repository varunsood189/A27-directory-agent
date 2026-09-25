# Bug 2 — Keystone contact_type vs roles.customer

**Book:** Keystone (`c1e47d8d-b849-4187-9a32-4103d3dece4a`) vs Suryodaya
**Date:** 2026-09-25, MCP `Party.list` / `Party.get`
**Status:** filed. In-app id `94be1601-6dd1-4ade-a01c-38317e39d9a1`.

## Re-measured totals

| | Suryodaya | Keystone |
|---|---|---|
| `Party.list` (no contact_type) | 194 | 100 |
| `contact_type=customer` | **44** | **0** |
| rows with `roles.customer` | 44 | **11** |
| `contact_type` null | 138 | **100** |
| `Party.list` arg `roles=customer` | JSON-RPC -32602, not an accepted argument | same |

Keystone sample with `roles.customer` and `contact_type` null: Allegheny Harvest Systems LLC (`62f8d1c3-1fc9-4e16-b967-1463c2c86936`). UI All Customers lists those 11.

Schema: `contact_type` enum `customer` / `vendor` / `both`. No `roles` filter on `Party.list`.

## Not this bug

Advertised `Party.list` defaults (`currency_id=locale:base_currency` → 0) and `search=%` matching the whole book are team20 platform reports. Do not re-file.
