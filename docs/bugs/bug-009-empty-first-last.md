# Bug 9 — Suryodaya first_name / last_name empty; sort_by first_name returns orgs

**Book:** Suryodaya. **Screen:** All Contacts, open a person (e.g. Aarti Bhosale).  
**Tool:** `Party.list`

## Repro

```
Party.list {limit: 100} → first_name empty on 100/100 of that page; last_name empty 100/100; name filled.
Party.list {sort_by: "first_name", limit: 3} → Bharat EV Motors Ltd, Kirloskar Pumps Ltd, Tata Ficosa (organizations).
Party.list {sort_by: "name", limit: 3} → Yogesh Khedkar, Yogesh Iyer, Vitthal Kale (people).
```

Keystone `sort_by=first_name` returns people who have first_name (Tom Reinholt, Tina Gallo, …).

## Paste (Suryodaya → All Contacts, open a person)

```
What I did: Suryodaya All Contacts. Opened a person (name filled). Party.list limit=100: first_name and last_name null on every row of the page. Party.list sort_by=first_name limit=3.

What I expected: first_name/last_name split from name, and sort_by=first_name to order people.

What happened: first_name and last_name empty. sort_by=first_name returns organizations (Bharat EV Motors Ltd, Kirloskar Pumps Ltd, Tata Ficosa). Company 5cbe5a55-af74-4363-a436-f5350593114c.
```
