import json
from pathlib import Path

from src.directory_agent import (
    DirectoryAgent,
    find_org,
    normalize_name,
    relationship_other_ids,
)
from src.mcp_client import McpClient, McpError
from src import settings

ROOT = Path(__file__).resolve().parents[1]


def _book(name):
    client = McpClient(
        settings.book_base(name),
        settings.email(),
        settings.book_password(name),
    )
    agent = DirectoryAgent(client, apply_writes=False)
    agent.connect()
    return client, agent


def test_aarti_deshpande_pair_gets_both_ids():
    client, agent = _book("suryodaya")
    page = client.call_tool("Party.list", {"search": "Aarti Deshpande", "limit": 20})
    rows = [
        r
        for r in (page.get("data") or [])
        if normalize_name(r.get("name")) == "aarti deshpande"
    ]
    assert len(rows) == 2
    names = {r.get("name") for r in rows}
    assert "Aarti Deshpande" in names
    assert "Aarti Deshpande (2)" in names
    got = []
    for row in rows:
        party = client.call_tool("Party.get", {"id": row["id"]})
        assert party.get("id") == row["id"]
        got.append(normalize_name(party.get("name")))
    assert set(got) == {"aarti deshpande"}


def test_suryodaya_relationship_total_is_zero():
    client, agent = _book("suryodaya")
    page = client.call_tool("PartyRelationship.list", {"limit": 1})
    assert int(page.get("total") or 0) == 0


def test_jsonrpc_error_is_still_http_200():
    client, agent = _book("keystone")
    try:
        client.call_tool("Party.get", {"id": "00000000-0000-0000-0000-000000000000"})
        assert False, "missing party should error"
    except McpError as err:
        assert client.calls[-1]["http"] == 200
        envelope = err.payload or {}
        assert "error" in envelope


def test_reget_after_list_still_returns_same_id():
    client, agent = _book("suryodaya")
    page = client.call_tool("Party.list", {"search": "Aarti Deshpande", "limit": 5})
    row = (page.get("data") or [])[0]
    first = client.call_tool("Party.get", {"id": row["id"]})
    second = client.call_tool("Party.get", {"id": row["id"]})
    assert first["id"] == second["id"] == row["id"]
    assert normalize_name(first.get("name")) == normalize_name(second.get("name"))


def test_godrej_agent_ids_equal_relationship_ids():
    client, agent = _book("suryodaya")
    result = agent.handle("Who do we know at Godrej Material Handling?")
    agent_ids = {person["id"] for person in result["who"] if person.get("id")}
    org = find_org(client, "Godrej Material Handling")
    db_ids = relationship_other_ids(client, org["id"]) if org and org.get("id") else set()
    assert agent_ids == db_ids == set()


def test_harness_journal_file_exists():
    from harness.run import run_task

    task = json.loads((ROOT / "harness" / "tasks" / "refuse_payroll.json").read_text())
    payload = run_task(task, settings.email())
    path = Path(payload["journal"])
    assert path.is_file()
    saved = json.loads(path.read_text())
    assert saved.get("outcome") in {"approve", "revise", "unevaluated"}
    assert saved.get("task_id") == "refuse_payroll"


def test_search_spaces_returns_zero():
    client, agent = _book("suryodaya")
    empty = client.call_tool("Party.list", {"search": "", "limit": 3})
    spaces = client.call_tool("Party.list", {"search": "   ", "limit": 3})
    assert int(empty.get("total") or 0) > 0
    assert int(spaces.get("total") or 0) == 0
