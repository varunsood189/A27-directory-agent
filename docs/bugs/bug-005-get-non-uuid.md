# Bug 5 — Party.get non-UUID is “not found”

**Book:** either. **Tool:** `Party.get`

## Repro

```
Party.get {id: "not-a-uuid"}
→ JSON-RPC -32602, message "Party not found.", data.code=not_found
```

Expected: invalid_arguments on `/id` (must be uuid). A malformed id is not a missing party.

## Paste (Keystone All Contacts)

```
What I did: team27. Party.get id=not-a-uuid.

What I expected: invalid_arguments, id must be a UUID.

What happened: Party not found (data.code=not_found). Same as a well-formed missing UUID. Company c1e47d8d-b849-4187-9a32-4103d3dece4a.
```
