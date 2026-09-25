# Bug 1 — 11 Active Customers vs Active (90d) empty

**Book:** Keystone (`c1e47d8d-b849-4187-9a32-4103d3dece4a`)
**Date:** 2026-09-24
**Screen:** All Contacts → Active (90d)
**Status:** filed in-app. Paste report id into `docs/bugs.md`.

## What we clicked

1. Keystone, All Contacts → All Customers: **Showing 11 records** (Allegheny Harvest Systems LLC, Angela Pruitt, Buckeye AgriPower, …). Every card **No activity**.
2. Click **Active (90d)**.

## What we saw

- Purple **CUSTOMER BASE** banner: **11 Active Customers**
- Sidebar **Active (90d) = 0** (while on that segment)
- **Showing 0 records** / No records in this segment
- Metric card Active (90d): **—**

Do not file the yellow “Financial context is not available” bar (no accounting locale).
