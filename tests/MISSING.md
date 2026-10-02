# Missing tests

The gap list from 2026-10-02 is now in pytest:

- `tests/test_spec_rest.py`
- `tests/test_bugs.py`
- `tests/test_boundary.py`

Still skipped on purpose:

- Bug 1 Active (90d) UI (not MCP)
- LLM / Ask Agent
- Files / Drive
- Concurrent live rename (writes stay off; re-get is covered instead)
