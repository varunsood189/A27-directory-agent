# Tests we will add (one at a time)

Seat 27 predicates first. Do not generate 100 files.

## Already there

- [x] `test_1.py` — normalize `(2)`, refuse words, blocked `contact_type`
- [x] `test_names.py` — normalize again
- [x] `test_who_predicate.py` — who-ids == relationship ids, Matt Swaim
- [x] `test_dedupe_predicate.py` — clusters + Party.get + Ajay not one cluster
- [x] `test_seat_queue.py` — refuse, Godrej, extra arg, associate=0
- [x] `test_handle_more.py` — trailing period, combined request, links [], missing get
- [x] `test_positive_negative.py` — 6 positive + 7 negative (`handle` / MCP)
- [x] `test_spec_rest.py` — `(2)` pair get, Suryodaya rel 0, HTTP 200 envelope, re-get, Godrej ids, journal file, spaces search
- [x] `test_bugs.py` — bugs 4, 6, 7, 8, 9
- [x] `test_boundary.py` — limit 0 / -1, offset -1, refuse parametrize, truncated password
- [ ] `test_2.py` — random words (optional)

## Do not add

- LLM / Ask Agent tests (there is no model)
- Files / Drive / payroll tools as if this seat owned them
- Bug 1 Active (90d) UI
