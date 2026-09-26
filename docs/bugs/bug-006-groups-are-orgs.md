# Bug 6 — Contact groups named for people hold only companies

**Books:** both. **Screen:** Contact Groups → Investors / Newsletter / VIP Clients.

## Repro

All 6 `ContactGroupMember` rows on each book; `Party.get` on each `party_id`:

| Group | Suryodaya members (all organization) | Keystone members (all organization) |
|---|---|---|
| Investors | Shreeji Powder Coating | Apex Metals Supply LLC |
| Newsletter | Jindal Steel Depot, Vardhman Aerospace SEZ Unit, Tata Ficosa | Cardinal Tillage Works, Tri-State Farm Equipment, Great Lakes Implement Co |
| VIP Clients | Kirloskar Pumps Ltd, Bharat EV Motors Ltd | Allegheny Harvest Systems LLC, Buckeye AgriPower Inc |

0 individuals in these groups.

## Paste (Keystone → Contact Groups → VIP Clients)

```
What I did: Keystone, Contact Groups. Opened VIP Clients, Newsletter, Investors. MCP ContactGroupMember.list + Party.get.

What I expected: people in groups named Investors / Newsletter / VIP Clients, or names that say they are company lists.

What happened: all 6 members are type=organization (VIP: Allegheny Harvest, Buckeye AgriPower). Same on Suryodaya (VIP: Kirloskar Pumps, Bharat EV Motors). No individuals. Company c1e47d8d-b849-4187-9a32-4103d3dece4a.
```
