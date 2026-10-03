# Tests

**54** pytest in this folder. Last full run: 54 passed.

```bash
cd "/home/varun/Documents/workspace/schoolofai/Assignment 20"
python3 -m pip install pytest
python3 -m pytest tests/ -q
```

Needs `.env` (gitignored) for live MCP tests. Do not `source .env`.

Spec the course asked you to type: [docs/test-spec.md](../docs/test-spec.md) (cases 1–18). File checklist: [TEST_PLAN.md](TEST_PLAN.md).

Not pytest (also required): `python3 harness/run.py` (5 tasks) and `python3 scripts/verify_live.py`.

## What each file covers

| File | Count | Covers |
|---|---|---|
| `test_1.py` | 3 | `normalize_name` `(2)`, refuse vs who, blocked `contact_type` |
| `test_names.py` | 1 | normalize Aarti `(2)` again |
| `test_2.py` | 4 | random suffix / refuse / extract (optional) |
| `test_who_predicate.py` | 1 | Hocking Hills who-ids == relationship ids, Matt Swaim |
| `test_dedupe_predicate.py` | 2 | clusters + `Party.get`; Ajay two people, not one merge |
| `test_seat_queue.py` | 4 | refuse no SalarySlip, Godrej empty, extra arg, associate=0 |
| `test_handle_more.py` | 4 | trailing period, combined request, `links []`, missing get |
| `test_positive_negative.py` | 13 | happy path + refuse / unknown company / bad id / blocked filters |
| `test_spec_rest.py` | 7 | `(2)` pair get, Suryodaya rel 0, HTTP 200, re-get, Godrej ids, journal, spaces search |
| `test_bugs.py` | 5 | bugs 4, 6, 7, 8, 9 |
| `test_boundary.py` | 10 | `limit` 0/−1, `offset` −1, refuse words, truncated password |

## Seat (must pass)

- Dedupe: `(2)` clusters still exist on `Party.get`; Ajay is not a merge
- Who: agent ids = `PartyRelationship` other-ids; Matt Swaim; Godrej empty
- Refuse: payroll/invoice; journal never calls `SalarySlip`

## Not in pytest

- Bug 1 Active (90d) UI
- Ask Agent / any LLM
- Files / Drive / payroll as if this seat owned them
