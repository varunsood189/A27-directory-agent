import os

import pytest

from src.directory_agent import DirectoryAgent, is_refusal_request
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


def test_party_list_limit_zero_keeps_total():
    client, agent = _book("suryodaya")
    page = client.call_tool("Party.list", {"limit": 0})
    assert int(page.get("total") or 0) > 0
    assert (page.get("data") or []) == []


def test_party_list_limit_negative_is_rejected():
    client, agent = _book("suryodaya")
    try:
        client.call_tool("Party.list", {"limit": -1})
        assert False, "limit -1 should fail"
    except McpError:
        assert client.calls[-1]["http"] == 200


def test_party_list_offset_negative_is_rejected():
    client, agent = _book("suryodaya")
    try:
        client.call_tool("Party.list", {"offset": -1, "limit": 1})
        assert False, "offset -1 should fail"
    except McpError:
        assert client.calls[-1]["http"] == 200


@pytest.mark.parametrize(
    "text",
    [
        "show payroll",
        "open the invoice",
        "salary slip please",
        "gst return for march",
        "work order 12",
        "payslip for april",
    ],
)
def test_refuse_words_parametrize(text):
    assert is_refusal_request(text) is True


def test_settings_prefers_file_when_shell_password_is_short(monkeypatch):
    file_vals = settings.parse_env_file(settings.ROOT / ".env")
    file_pw = file_vals.get("AS_PASSWORD_KEYSTONE")
    if not file_pw:
        pytest.skip("no .env password")
    short = file_pw[:16]
    if len(file_pw) <= len(short):
        pytest.skip("file password is not longer than 16")
    monkeypatch.setenv("AS_PASSWORD_KEYSTONE", short)
    got = settings.get("AS_PASSWORD_KEYSTONE")
    assert got == file_pw
    assert len(got) > len(os.environ.get("AS_PASSWORD_KEYSTONE") or "")
