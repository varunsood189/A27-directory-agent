# Bug 8 — Suryodaya AddressBooks empty (5 of 8)

**Book:** Suryodaya. **Screen:** Address Books  
**Tool:** `AddressBook.list` + `AddressBookEntry.list`

## Repro

8 books, 8 entries. Entries only in Suppliers (2), Team (3), Personal (3). These 5 have **0** entries:

Suppliers — Purchasing; Transporters — Quality; Service Vendors — Stores; Customers — Press Shop; Service Vendors — Accounts.

Keystone has only the 3 populated books (Suppliers, Team, Personal).

## Paste (Suryodaya → Address Books)

```
What I did: Suryodaya, Address Books. AddressBook.list total=8, AddressBookEntry.list total=8. Opened Suppliers — Purchasing.

What I expected: each named book to have entries, or only the three populated books to exist (as on Keystone).

What happened: 5 departmental books have 0 entries. All 8 entries are in Suppliers, Team, Personal. Company 5cbe5a55-af74-4363-a436-f5350593114c.
```
