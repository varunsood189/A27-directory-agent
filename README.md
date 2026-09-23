# AgentSwitch Directory seat (team27 / A27)

**Week 1 for the teacher:** [`docs/gap-report.md`](docs/gap-report.md)

One agent on this machine, driving Directory over MCP.

> Deduplicate the customer list, and tell me who we know at this company.

## Run

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

Writes to the shared party list are off unless `APPLY_WRITES=1`. Default is identify + re-get.

## What is in this repo

| Path | What |
|---|---|
| `docs/gap-report.md` | Week 1. Attio vs Directory. |
| `docs/domain-map.md` | Live Party / relationships. |
| `docs/test-spec.md` | Cases **you** type as pytest. Generated tests score 0. |
| `src/` | MCP client + Directory agent. |
| `harness/` | Tasks, predicates on `Party.get`, journals under `runs/`. |

Do not wrap `GET /api/agent/tools`. Do not `PUT /api/accounting/locale`.
