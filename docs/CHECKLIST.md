# Capstone checklist — Seat 27 Directory

Tick in order. Due **Tue 6 Oct 2026, 13:00**. Seat is **Directory**, not Files.

## Already done

- [x] Seat 27 Directory (not Files). Group A27. Login `team27@…`
- [x] Gap report vs Attio — `docs/gap-report.md`
- [x] MCP agent both books — `src/` (`POST /api/mcp` only)
- [x] Graded request: dedupe + who-we-know
- [x] Refuse payroll (no `SalarySlip`)
- [x] Harness 5 tasks, live ids, journals — **5/5 approve 3 Oct 2026**
- [x] 10 Directory bugs filed in-app — `docs/bugs.md`
- [x] Public GitHub — https://github.com/varunsood189/A27-directory-agent
- [x] Axiom Session 20 form (26 Sep) — same URL + caption + incognito
- [x] Suryodaya **Harness** button saved (3 Oct 11:42)
- [x] `.env` gitignored. `APPLY_WRITES=0`. No locale PUT in code

## You still do (required)

- [x] **Keystone Harness button** — https://class.agentswitch.theschoolofai.in → Harness → same GitHub, branch `main`
- [x] **Suryodaya branch** — Edit harness card, set Branch to `main` if it still shows `—`
- [x] **A27 group** — post: harness GitHub URL + 5/5 approve (they said they see no harness in chat)
- [x] **Type tests** — `tests/test_me.py` (normalize, refuse, blocked contact_type)
- [x] **Password comment** — no password in `src/settings.py`
- [x] **Incognito check** — open the GitHub URL with no login; it must load

## Do not do

- [ ] Ask Agent / LLM / `GET /api/agent/tools`
- [ ] `PUT /api/accounting/locale` (does not join the two books)
- [ ] File 403 / missing payroll tools / `GET /api/mcp` 405 / team20 Files bugs
- [ ] Tidy other teams’ contacts. `APPLY_WRITES=1` unless you mean it
- [ ] Generate 100 more pytest files

## Optional

- [ ] Push `docs/index.html` + README test list so GitHub matches your laptop
- [ ] Re-run `python3 harness/run.py` if they ask for a fresh journal
- [ ] Axiom resubmit if you push after 26 Sep (resubmission allowed)
