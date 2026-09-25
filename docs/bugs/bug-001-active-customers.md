# Bug 1 evidence — 11 Active Customers vs Active (90d) empty

**Seat:** 27 Directory. **Book:** Keystone. **Company:** `c1e47d8d-b849-4187-9a32-4103d3dece4a`
**Date:** 2026-09-24
**Tool / screen:** All Contacts → Active (90d)
**Severity:** Medium
**Report id:** not recovered (filed; do not re-file)

## Repro

1. Keystone, All Contacts → **All Customers**: Showing **11** records (Allegheny Harvest Systems LLC, Angela Pruitt, Buckeye AgriPower, …). Every card **No activity**.
2. Click **Active (90d)**.

## Result

| Surface | Value |
|---|---|
| Purple CUSTOMER BASE banner | **11 Active Customers** |
| Sidebar Active (90d), while that segment is selected | **0** |
| List | Showing **0** records / No records in this segment |
| Active (90d) metric card | **—** |

Expected: heading, sidebar count, and list agree.

Not this bug: yellow “Financial context is not available” bar (no accounting locale).
