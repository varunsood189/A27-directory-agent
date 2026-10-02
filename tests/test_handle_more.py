from src.directory_agent import DirectoryAgent, normalize_name
from src.mcp_client import McpClient, McpError
from src import settings


def _keystone():
    client = McpClient(
        settings.book_base("keystone"),
        settings.email(),
        settings.book_password("keystone"),
    )
    agent = DirectoryAgent(client, apply_writes=False)
    agent.connect()
    return client, agent


def test_who_trailing_period_still_finds_matt():
    client, agent = _keystone()
    result = agent.handle("Who do we know at Hocking Hills Mower Works.")
    assert result["refused"] is False
    names = {normalize_name(p.get("name")) for p in result["who"]}
    assert "matt swaim" in names


def test_combined_request_has_who_and_not_refused():
    client, agent = _keystone()
    result = agent.handle(
        "Deduplicate the customer list, and tell me who we know at Hocking Hills Mower Works?"
    )
    assert result["refused"] is False
    names = {normalize_name(p.get("name")) for p in result["who"]}
    assert "matt swaim" in names


def test_dedupe_links_empty_when_writes_off():
    client, agent = _keystone()
    result = agent.handle("Deduplicate the customer list.")
    for cluster in result["clusters"]:
        assert cluster.get("links") == []


def test_missing_party_get_raises():
    client, agent = _keystone()
    try:
        client.call_tool("Party.get", {"id": "00000000-0000-0000-0000-000000000000"})
        assert False, "missing party should error"
    except McpError:
        pass
