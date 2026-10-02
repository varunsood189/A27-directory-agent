from src.directory_agent import DirectoryAgent
from src.mcp_client import McpClient, McpError
from src import settings


def _book(name):
    client = McpClient(
        settings.book_base(name),
        settings.email(),
        settings.book_password(name),
    )
    agent = DirectoryAgent(client, apply_writes=False)
    agent.connect()
    return client, agent


def test_missing_party_not_found_uses_minus_32602():
    client, agent = _book("keystone")
    try:
        client.call_tool("Party.get", {"id": "00000000-0000-0000-0000-000000000000"})
        assert False, "missing party should error"
    except McpError as err:
        envelope = err.payload or {}
        rpc = envelope.get("error") or {}
        assert rpc.get("code") == -32602
        data = rpc.get("data") or {}
        assert data.get("code") == "not_found"


def test_contact_group_members_are_organizations():
    client, agent = _book("suryodaya")
    page = client.call_tool("ContactGroupMember.list", {"limit": 50})
    rows = page.get("data") or []
    assert len(rows) >= 1
    for row in rows:
        party = client.call_tool("Party.get", {"id": row["party_id"]})
        assert party.get("type") == "organization"


def test_suryodaya_has_empty_contact_groups():
    client, agent = _book("suryodaya")
    groups = client.call_tool("ContactGroup.list", {"limit": 50})
    members = client.call_tool("ContactGroupMember.list", {"limit": 50})
    assert int(groups.get("total") or 0) == 12
    assert int(members.get("total") or 0) == 6
    filled = {row.get("group_id") for row in (members.get("data") or [])}
    empty = [g for g in (groups.get("data") or []) if g.get("id") not in filled]
    assert len(empty) == 9


def test_suryodaya_has_empty_address_books():
    client, agent = _book("suryodaya")
    books = client.call_tool("AddressBook.list", {"limit": 50})
    entries = client.call_tool("AddressBookEntry.list", {"limit": 50})
    assert int(books.get("total") or 0) == 8
    assert int(entries.get("total") or 0) == 8
    filled = {row.get("address_book_id") for row in (entries.get("data") or [])}
    empty = [b for b in (books.get("data") or []) if b.get("id") not in filled]
    assert len(empty) == 5


def test_suryodaya_person_missing_first_last():
    client, agent = _book("suryodaya")
    page = client.call_tool("Party.list", {"type": "individual", "limit": 20})
    people = [r for r in (page.get("data") or []) if r.get("type") == "individual"]
    assert people
    blank = [
        r
        for r in people
        if r.get("name") and not r.get("first_name") and not r.get("last_name")
    ]
    assert len(blank) >= 1
    sorted_fn = client.call_tool("Party.list", {"sort_by": "first_name", "limit": 3})
    rows = sorted_fn.get("data") or []
    assert rows
    assert all(r.get("type") == "organization" for r in rows)
