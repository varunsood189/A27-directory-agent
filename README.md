# Directory Agent — AgentSwitch (Team 27)

Seat **27 · Directory**. Contacts spine (`Party` / `PartyRelationship`). One MCP agent for both books.

> Deduplicate the customer list, and tell me who we know at this company.

Goals: `directory.deduplicate_customers`, `directory.who_do_we_know`.

## Week 1 — Gap report

- [Gap report vs Attio](docs/gap-report.md)
- [Bugs](docs/bugs.md) — 4 filed, 6 to-file
- [Domain map](docs/domain-map.md)

## Agent + harness

MCP only (`POST /api/mcp`). Both books. Writes off unless `APPLY_WRITES=1`.

```bash
export AS_SURYODAYA=https://agentswitch.theschoolofai.in
export AS_KEYSTONE=https://class.agentswitch.theschoolofai.in
export AS_EMAIL=team27@theschoolofai.in
export AS_PASSWORD_SURYODAYA='…'
export AS_PASSWORD_KEYSTONE='…'

python3 src/run_agent.py --book suryodaya
python3 src/run_agent.py --book keystone --request "Who do we know at Hocking Hills Mower Works?"
python3 harness/run.py
```

| Path | What |
|---|---|
| `src/` | MCP client + Directory agent |
| `harness/` | Five tasks, two books. Who-we-know scored by relationship id sets. Journals under `runs/` |
| `docs/test-spec.md` | Cases **you** type as pytest. Generated tests score 0. |

Do not wrap `GET /api/agent/tools`. Do not `PUT /api/accounting/locale`. Do not re-file team20 Files/platform reports.
