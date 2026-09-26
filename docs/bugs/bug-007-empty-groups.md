# Bug 7 — Suryodaya ContactGroups empty (9 of 12)

**Book:** Suryodaya `5cbe5a55-af74-4363-a436-f5350593114c`  
**Screen:** Contact Groups  
**Tool:** `ContactGroup.list` + `ContactGroupMember.list`  
**Report id:** `24977785-8824-4e22-8aff-e4d719b56dcc`

## Repro

12 groups, 6 members. Members only in Investors (1), Newsletter (3), VIP Clients (2). These 9 have **0** members:

Newsletter subscribers — Stores / Fabrication / Press Shop; Key customers — Purchasing / Quality; Transporters — Purchasing; Approved suppliers — Maintenance / Sales Desk; Service partners — Press Shop.

## Paste (Suryodaya → Contact Groups)

```
What I did: Suryodaya, team27. Contact Groups. Counted groups vs members. ContactGroup.list total=12, ContactGroupMember.list total=6.

What I expected: departmental groups (Key customers — Purchasing, Newsletter subscribers — Stores, …) to have members, or not to exist.

What happened: 9 of 12 groups have 0 members. All 6 members are in Investors, Newsletter, VIP Clients. Company 5cbe5a55-af74-4363-a436-f5350593114c.
```
