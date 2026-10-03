# Directory Agent — AgentSwitch (Team 27)

Seat **27 · Directory**. Contacts spine (`Party` / `PartyRelationship`). One MCP agent for both books.

> Deduplicate the customer list, and tell me who we know at this company.

Goals: `directory.deduplicate_customers`, `directory.who_do_we_know`.

## Week 1 — Gap report

- [Gap report vs Attio](docs/gap-report.md)
- [Bugs](docs/bugs.md) — **10 filed**
- [Completeness audit](docs/completeness-audit.md)
- [One-page HTML](docs/index.html) — open in a browser (tests, bugs, how to run)

## Agent + harness

MCP only (`POST /api/mcp`). Both books. Writes off unless `APPLY_WRITES=1`.

```bash
# Passwords live in .env (gitignored). Do not `source .env` — bash strips `!`.
python3 src/run_agent.py --book keystone --request "Who do we know at Hocking Hills Mower Works?"
python3 src/run_agent.py --book suryodaya
python3 harness/run.py
```

| Path | What |
|---|---|
| `src/` | MCP client + Directory agent |
| `harness/` | Five tasks, two books. Who-we-know scored by relationship id sets. Journals under `runs/` |
| `tests/` | **54** pytest. Seat predicates, spec 1–18, filed MCP bugs. [List](tests/README.md). Spec: [docs/test-spec.md](docs/test-spec.md) |
| `scripts/verify_live.py` | Extra live smokes (not pytest) |

```bash
python3 -m pytest tests/ -q
python3 scripts/verify_live.py
```

Do not wrap `GET /api/agent/tools`. Do not `PUT /api/accounting/locale`. Do not re-file team20 Files/platform reports. Ask Agent is not assigned to team27 — run this repo instead.
