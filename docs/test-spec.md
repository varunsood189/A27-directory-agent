# tests you must type

A test written by Claude or Codex scores **zero**. Do not copy these into `tests/` by asking an agent to generate pytest.

Type your own files. Ten points each. Suggested cases (you write the code):

1. `Party.list` search `Ajay` returns two ids; they are not a merge cluster.
2. A name with `(2)` shares `normalize_name` with the unsuffixed row; `Party.get` both ids still work.
3. Keystone `PartyRelationship.list` for Hocking Hills includes Matt Swaim; who-list ids equal that set. Suryodaya relationship total can be 0.
4. Refusal request never calls `SalarySlip` / payroll tools (inspect the journal).
5. JSON-RPC error is still HTTP 200 — client must read `error` in the envelope.
6. Extra MCP argument is rejected (`additionalProperties: false`).
7. After a concurrent rename, the harness re-gets ids before scoring.
8. `contact_type=customer` is not treated as the customer list on Keystone.

Journal path: `runs/<book>/<task_id>/*.json` must exist before the outcome is set.
