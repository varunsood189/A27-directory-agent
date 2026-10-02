from src.directory_agent import DirectoryAgent
from src.mcp_client import McpClient, McpError
from src import settings


def _suryodaya():
    client = McpClient(
        settings.book_base("suryodaya"),
        settings.email(),
        settings.book_password("suryodaya"),
    )
    agent = DirectoryAgent(client, apply_writes=False)
    agent.connect()
    return client, agent


def _keystone():
    client = McpClient(
        settings.book_base("keystone"),
        settings.email(),
        settings.book_password("keystone"),
    )
    agent = DirectoryAgent(client, apply_writes=False)
    agent.connect()
    return client, agent


def test_refuse_payroll_no_salary_tools():
    client, agent = _suryodaya()
    result = agent.handle("List this month's salary slips and explain why one net pay changed.")
    assert result["refused"] is True
    assert result["who"] == []
    assert result["clusters"] == []
    tools = [c.get("tool") or "" for c in client.calls]
    assert not any("SalarySlip" in t or "Payroll" in t for t in tools)


def test_godrej_who_is_empty():
    client, agent = _suryodaya()
    result = agent.handle("Who do we know at Godrej Material Handling?")
    assert result["refused"] is False
    assert result["who"] == []


def test_extra_mcp_arg_is_rejected():
    client, agent = _keystone()
    try:
        client.call_tool("Party.list", {"limit": 1, "not_a_real_field": True})
        assert False, "extra arg should fail"
    except McpError:
        pass


def test_associate_filter_zeros_keystone_graph():
    client, agent = _keystone()
    none = client.call_tool("PartyRelationship.list", {"limit": 5})
    assoc = client.call_tool("PartyRelationship.list", {"relationship": "associate", "limit": 5})
    assert int(none.get("total") or 0) > 0
    assert int(assoc.get("total") or 0) == 0
