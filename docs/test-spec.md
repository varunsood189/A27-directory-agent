# tests you must type

A test written by Claude or Codex scores **zero**. Do **not** copy generated pytest into `tests/`. Type the files yourself. Ten points each.

The live battery that is **not** pytest (already passing harness + extra smokes):

```bash
python3 harness/run.py
python3 scripts/verify_live.py
```

## Cases to type (you write `tests/test_*.py`)

1. `Party.list` search `Ajay` returns two ids; they are not a merge cluster.
2. A name with `(2)` shares `normalize_name` with the unsuffixed row; `Party.get` both ids still work.
3. Keystone `PartyRelationship.list` for Hocking Hills includes Matt Swaim; who-list ids equal that set. Suryodaya relationship total can be 0.
4. Refusal request never calls `SalarySlip` / payroll tools (inspect the journal).
5. JSON-RPC error is still HTTP 200 — client must read `error` in the envelope.
6. Extra MCP argument is rejected (`additionalProperties: false`).
7. After a concurrent rename, the harness re-gets ids before scoring.
8. `contact_type=customer` is not treated as the customer list on Keystone.
9. `normalize_name("Aarti Deshpande (2)") == "aarti deshpande"`.
10. `is_refusal_request` is true for payroll / invoice / salary; false for who-we-know.
11. `party_list_args({"contact_type": "customer"})` raises.
12. `PartyRelationship.list` with `relationship=associate` total 0 on Keystone; omit filter total > 0.
13. Who-we-know with a trailing period still finds Hocking Hills / Matt Swaim.
14. Godrej who-we-know: agent ids == relationship ids == empty; no invented names.
15. Dedupe with `APPLY_WRITES=0` leaves `links == []`.
16. Journal path `runs/<book>/<task_id>/*.json` exists before outcome is set.
17. `Party.get` missing UUID: envelope has `error` (HTTP still 200).
18. Search of only spaces is not treated as “list everyone” if you assert MCP totals (optional; filed as bug 10).

Journal path: `runs/<book>/<task_id>/*.json` must exist before the outcome is set.

Do not generate 100 pytest files. The brief zeros agent-written tests. Type a handful of the cases above; the harness + `scripts/verify_live.py` is the live proof.
