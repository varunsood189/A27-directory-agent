# Bug 4 — not_found uses JSON-RPC -32602

**Books:** both. **Tools:** `Party.get`, `AddressBook.get`, `ContactGroup.get`, `PartyRelationship.get`  
**Report id:** `d8ec8e3e-a74a-4a6b-9b9b-e858983d1b15`

## Repro

```
Party.get {id: "00000000-0000-0000-0000-000000000000"}
→ JSON-RPC error code -32602, message "Party not found.", data.code=not_found
```

Same -32602 + not_found for AddressBook.get, ContactGroup.get, PartyRelationship.get on a zero UUID.

-32602 is invalid params. A missing row is not invalid params.

## Paste (Keystone All Contacts)

```
What I did: team27. Party.get id=00000000-0000-0000-0000-000000000000. Same pattern on AddressBook.get, ContactGroup.get, PartyRelationship.get.

What I expected: not_found with a not-found JSON-RPC code (or HTTP 404 in the envelope), not invalid params.

What happened: code -32602 (invalid params), message Party not found, data.code=not_found. Company c1e47d8d-b849-4187-9a32-4103d3dece4a.
```
