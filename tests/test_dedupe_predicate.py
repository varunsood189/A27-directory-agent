from src.directory_agent import DirectoryAgent, normalize_name
from src.mcp_client import McpClient
from src import settings


def test_dedupe_clusters_still_exist_on_party_get():
    client = McpClient(
        settings.book_base("suryodaya"),
        settings.email(),
        settings.book_password("suryodaya"),
    )
    agent = DirectoryAgent(client, apply_writes=False)
    agent.connect()

    result = agent.handle("Deduplicate the customer list.")

    # YOU: the request is in-seat, so refused must be False
    assert result["refused"] is False

    clusters = result["clusters"]
    # YOU: there must be at least one cluster
    assert len(clusters) >= 1

    confirmed = 0
    for cluster in clusters:
        ids = cluster["member_ids"]
        if len(ids) < 2:
            continue
        names = []
        for pid in ids:
            row = client.call_tool("Party.get", {"id": pid})
            # YOU: Party.get must return a row (id still exists)
            assert row is not None
            assert row.get("id") == pid
            names.append(normalize_name(row.get("name")))
        # YOU: all members in one cluster share one base name
        assert len(set(names)) == 1
        confirmed += 1

    # YOU: at least one cluster was checked
    assert confirmed >= 1


def test_ajay_bansode_and_iyer_are_not_one_cluster():
    """YOU write this one. Same connect as above. Search Ajay. Two people, not one merge."""
    client = McpClient(
        settings.book_base("suryodaya"),
        settings.email(),
        settings.book_password("suryodaya"),
    )
    agent = DirectoryAgent(client, apply_writes=False)
    agent.connect()

    page = client.call_tool("Party.list", {"search": "Ajay", "limit": 50})
    rows = page.get("data") or []

    ids = [r["id"] for r in rows]
    assert len(ids) == 2

    clusters = agent.deduplicate()
    for cluster in clusters:
        member_ids = set(cluster["member_ids"])
        assert not set(ids).issubset(member_ids)
