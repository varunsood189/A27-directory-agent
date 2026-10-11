# Local tests (laptop)

Always from the project folder. **Do not** `source .env` (bash strips `!` → 401). Python reads `.env` itself.

```bash
cd "/home/varun/Documents/workspace/schoolofai/Assignment 20"
```

Need `.env` with both book passwords (see `.env.example`). `APPLY_WRITES=0`.

---

## 1. Fast — no login (~1s)

Official `results.json` shape + name/refuse helpers.

```bash
python3 -m pytest tests/test_harness_contract.py tests/test_me.py tests/test_1.py tests/test_names.py tests/test_2.py -q
```

Expect: all passed.

---

## 2. One live request (~20s)

```bash
python3 src/run_agent.py --book keystone --request "Who do we know at Hocking Hills Mower Works?"
python3 src/run_agent.py --book suryodaya --request "Deduplicate the customer list."
python3 src/run_agent.py --book keystone --request "Show me the payroll and salary slips."
```

Expect: Matt Swaim; `(2)` clusters with `"links": []`; `"refused": true`.

---

## 3. Local harness — five tasks (~3–6 min)

This is **your** scorer (`outcome: approve`). Uses `.env` login.

```bash
python3 harness/run.py
```

One task:

```bash
python3 harness/run.py --task who_hocking_hills
python3 harness/run.py --task refuse_payroll
python3 harness/run.py --task deduplicate_customers
```

Expect every line `"outcome": "approve"`. Journals: `runs/<book>/<task_id>/`.

---

## 4. Official-shape runner (what the server runs)

Needs `AGENTSWITCH_BASE_URL` + `AGENTSWITCH_TOKEN` (no password in the command). Get a token from login, then run **one instance**:

```bash
python3 - <<'PY'
from src.mcp_client import McpClient
from src import settings
book = "keystone"  # or "suryodaya"
c = McpClient(settings.book_base(book), settings.email(), settings.book_password(book))
c.login()
print(settings.book_base(book))
print("token_len", len(c.token or ""))
open("/tmp/as_token", "w").write(c.token or "")
PY

export AGENTSWITCH_BASE_URL="https://class.agentswitch.theschoolofai.in"   # keystone
# export AGENTSWITCH_BASE_URL="https://agentswitch.theschoolofai.in"       # suryodaya
export AGENTSWITCH_TOKEN="$(cat /tmp/as_token)"
export AGENTSWITCH_INSTANCE=keystone   # or suryodaya
python3 -m harness.runner
cat results.json
```

On the laptop the **model loop is skipped** (no `OPENAI_API_KEY`). Directory tasks should still `passed: true`. On 11 Oct the server injects OpenAI keys.

Do **not** print or commit the token. Delete `/tmp/as_token` after.

---

## 5. Full live pytest (slow, ~6 min)

```bash
python3 -m pytest tests/ -q
```

Needs `.env`. Skip this if you only want a quick check — use **1** then **3**.

---

## Do not

- `source .env`
- `PUT /api/accounting/locale`
- Click **Submit for a run** twice (one run / 3 days). Local tests do not use that quota.
