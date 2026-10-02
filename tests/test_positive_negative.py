import pytest

from src.directory_agent import (
    DirectoryAgent,
    extract_company,
    is_refusal_request,
    normalize_name,
    party_list_args,
)
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


def test_positive_extract_hocking_hills_name():
    got = extract_company("Who do we know at Hocking Hills Mower Works?")
    assert got == "Hocking Hills Mower Works"


def test_positive_who_request_is_not_refusal():
    assert is_refusal_request("Who do we know at Hocking Hills Mower Works?") is False


def test_positive_keystone_party_list_has_rows():
    client, agent = _book("keystone")
    page = client.call_tool("Party.list", {"limit": 1})
    assert int(page.get("total") or 0) > 0


def test_positive_represents_graph_has_rows():
    client, agent = _book("keystone")
    page = client.call_tool("PartyRelationship.list", {"relationship": "represents", "limit": 5})
    assert int(page.get("total") or 0) > 0


def test_positive_who_handle_returns_people():
    client, agent = _book("keystone")
    result = agent.handle("Who do we know at Hocking Hills Mower Works?")
    assert result["refused"] is False
    assert len(result["who"]) >= 1


def test_positive_suryodaya_dedupe_finds_clusters():
    client, agent = _book("suryodaya")
    result = agent.handle("Deduplicate the customer list.")
    assert result["refused"] is False
    assert len(result["clusters"]) >= 1


def test_negative_refuse_invoice():
    client, agent = _book("keystone")
    result = agent.handle("Open this invoice and tell me the GST.")
    assert result["refused"] is True
    assert result["who"] == []
    assert result["clusters"] == []


def test_negative_refuse_work_order():
    assert is_refusal_request("show the work order") is True


def test_negative_unknown_company_does_not_invent_people():
    client, agent = _book("keystone")
    result = agent.handle("Who do we know at ZzNotARealCompanyZz?")
    assert result["refused"] is False
    assert result["who"] == []


def test_negative_party_get_not_a_uuid():
    client, agent = _book("keystone")
    with pytest.raises(McpError):
        client.call_tool("Party.get", {"id": "not-a-uuid"})


def test_negative_blocked_currency_default_filter():
    with pytest.raises(ValueError):
        party_list_args({"currency_id": "locale:base_currency"})


def test_negative_contact_type_customer_on_keystone_is_zero():
    client, agent = _book("keystone")
    page = client.call_tool("Party.list", {"contact_type": "customer", "limit": 1})
    assert int(page.get("total") or 0) == 0


def test_negative_normalize_does_not_keep_suffix():
    assert normalize_name("Anil Bhosale (3)") != "anil bhosale (3)"
    assert normalize_name("Anil Bhosale (3)") == "anil bhosale"
