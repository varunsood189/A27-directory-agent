# Bug 10 — Party.list search of only spaces returns 0

**Books:** both (Suryodaya 194→0, Keystone 100→0).  
**Screen:** All Contacts search box.  
**Tool:** `Party.list`  
**Report id:** `33506af1-d415-4a19-a6e0-01544e939c0f`

## Repro

```
Party.list {search: "", limit: 3}     → total=194 (Suryodaya) / 100 (Keystone)
Party.list {search: "   ", limit: 3} → total=0
```

Whitespace-only search is treated as a real query and matches nothing, instead of as “no search”.

## Paste (Suryodaya → All Contacts)

```
What I did: Suryodaya All Contacts. Search box empty: list has records. Typed only spaces. MCP: Party.list search="" total=194; search="   " total=0. Keystone same (100 vs 0).

What I expected: spaces-only search to behave like no search.

What happened: total=0. Company 5cbe5a55-af74-4363-a436-f5350593114c.
```
