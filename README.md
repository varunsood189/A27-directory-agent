# Directory Agent

MCP agent that deduplicates a CRM contacts graph and answers “who do we know at this company?” — with a scored harness and **54 pytest**.

> Recruiter takeaway: real MCP tool-calling agent (not a chatbot demo), live schema workarounds, predicate-scored harness, and a large automated test suite.

## Problem

Accounting/CRM books expose a contacts spine (`Party` / `PartyRelationship`) over MCP, but the data is messy: duplicate display names (`Aarti Deshpande (2)`), empty relationship graphs on some books, and filters that look valid in the schema yet return zero rows. Graded goals are simple in words and hard in practice:

- **Deduplicate customers** — cluster near-duplicate parties without inventing merges the API does not support.
- **Who do we know?** — return people linked to a company via relationship edges, or correctly report empty.
- **Refuse** out-of-scope asks (payroll, invoices, work orders) without calling the wrong tools.

## Approach

- **MCP-only client** (`POST /api/mcp`) — `Party.list` / `Party.get` / `PartyRelationship.list`; writes gated behind `APPLY_WRITES=1`.
- **Schema-aware agent** — blocks filters that zero Keystone (`contact_type`, defaults), pages parties, clusters on normalized names (strip `(2)`/`(3)`), re-gets before any write, and scores “who we know” against an independent relationship-id set.
- **Harness** — five tasks across two books; journals under `runs/`; predicates for dedupe / who / refuse.
- **Tests** — **54 pytest** covering seat predicates, filed MCP bugs, harness contract, and positive/negative cases ([list](tests/README.md), [spec](docs/test-spec.md)).

```text
request ──► DirectoryAgent ──► McpClient ──► Party / PartyRelationship
                 │
                 ▼
            harness predicates + pytest
```

## Demo / results

```bash
# Deduplicate / who-we-know against a live book (credentials in .env)
python3 src/run_agent.py --book keystone --request "Who do we know at Hocking Hills Mower Works?"
python3 src/run_agent.py --book suryodaya

# Scored harness (journals → runs/)
python3 harness/run.py

# Official AgentSwitch harness submit (token auth; no book passwords)
python -m harness.runner

# Unit + live MCP suite
python3 -m pytest tests/ -q   # 54 tests
```

What works end-to-end when credentials are present:

| Capability | Evidence |
|---|---|
| Who-we-know (Keystone) | Agent person ids match `PartyRelationship` other-ids (e.g. Hocking Hills → Matt Swaim) |
| Empty graph honesty | Godrej / Suryodaya relationship totals handled without inventing contacts |
| Dedupe without false merges | `(2)` clusters still exist on `Party.get`; distinct people not collapsed |
| Refusal | Payroll/invoice language never triggers `SalarySlip` / wrong apps |
| Engineering discipline | **54 pytest**, 10 filed MCP bugs, gap report vs Attio CRM |

Browseable summary: [docs/index.html](docs/index.html).

## Quick start

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt pytest
cp .env.example .env   # fill AS_PASSWORD_* ; do not `source .env` (bash strips `!`)
python3 -m pytest tests/ -q
```

Local how-to (does **not** burn the official 3-day harness window): [docs/local-test.md](docs/local-test.md).

| Path | What |
|---|---|
| `src/` | MCP client + Directory agent |
| `harness/` | Five tasks, two books, predicate scoring |
| `tests/` | **54** pytest |
| `scripts/verify_live.py` | Extra live smokes (not pytest) |
| `docs/` | Gap report, bugs, completeness audit, test spec |

## Stack

Python · MCP (JSON-RPC over HTTP) · pytest · OpenAI-compatible model loop (official harness) · dotenv

## Course context (optional)

Built for AgentSwitch Directory seat work (team 27). Course checklists and LMS notes live under `docs/` — they are not the product story above.
