from src.directory_agent import (
    DirectoryAgent,
    find_org,
    normalize_name,
    relationship_other_ids,
)
from src.mcp_client import McpClient
from src import settings


def test_who_hocking_hills_ids_match_relationships():
    client = McpClient(
        settings.book_base("keystone"),
        settings.email(),
        settings.book_password("keystone"),
    )
    agent = DirectoryAgent(client, apply_writes=False)
    agent.connect()

    result = agent.handle("Who do we know at Hocking Hills Mower Works?")
    assert result["refused"] is False

    agent_ids = {person["id"] for person in result["who"]}
    org = find_org(client, "Hocking Hills Mower Works")
    db_ids = relationship_other_ids(client, org["id"])

    assert agent_ids == db_ids
    assert len(agent_ids) > 0

    names = set()
    for pid in agent_ids:
        row = client.call_tool("Party.get", {"id": pid})
        names.add(normalize_name(row.get("name")))
    assert "matt swaim" in names
