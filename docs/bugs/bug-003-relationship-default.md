# Bug 3 — PartyRelationship.list default `associate` zeros Keystone

**Book:** Keystone `c1e47d8d-b849-4187-9a32-4103d3dece4a`  
**Tool:** `PartyRelationship.list`  
**File from:** Keystone **All Contacts**. Do **not** use Ask Agent (seat not assigned). Repro is MCP `PartyRelationship.list`.  
**Report id:** `a9a923b6-ce45-482f-8f8b-3aebabc9ee03`

## Repro

```
PartyRelationship.list {limit: 5}                         → total=28 (all relationship=represents)
PartyRelationship.list {relationship: "associate", limit: 5} → total=0
PartyRelationship.list {relationship: "represents", limit: 5} → total=28
```

Schema default: `relationship: "associate"`. An agent that sends advertised defaults finds nobody at Hocking Hills.

Suryodaya graph is already 0, so the default is invisible there.

## Paste

```
What I did: Keystone, team27. PartyRelationship.list with no relationship filter (total=28, all represents, includes Matt Swaim → Hocking Hills). Then PartyRelationship.list relationship=associate (the schema default).

What I expected: default associate to mean “do not filter”, or the live edges to be associate. Who-we-know should still see Matt Swaim.

What happened: relationship=associate total=0. Omit the field, total=28. Company c1e47d8d-b849-4187-9a32-4103d3dece4a.
```
