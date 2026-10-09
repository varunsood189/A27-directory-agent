"""Official Our-harness contract. No live MCP. Match theschoolofai/agentswitch-harness-example."""

from pathlib import Path

from harness.runner import TASKS, record, write_results

ROOT = Path(__file__).resolve().parents[1]


def test_toml_is_at_repo_root():
    path = ROOT / "agentswitch-harness.toml"
    text = path.read_text()
    assert 'install = "pip install -r requirements.txt"' in text
    assert 'run     = "python -m harness.runner"' in text or 'run = "python -m harness.runner"' in text
    assert 'results = "results.json"' in text
    assert "suryodaya" in text
    assert "keystone" in text
    assert "timeout_minutes" in text


def test_requirements_has_openai():
    text = (ROOT / "requirements.txt").read_text()
    assert "openai" in text


def test_record_shape_matches_official_results():
    TASKS.clear()
    record("mcp_tools_list", "MCP tools/list works with the seat token", True, "205 tools", "keystone")
    row = TASKS[0]
    assert row["id"] == "keystone:mcp_tools_list"
    assert row["title"]
    assert row["passed"] is True
    assert row["score"] == 1.0
    assert isinstance(row["evidence"], str)


def test_write_results_json_schema(tmp_path, monkeypatch):
    TASKS.clear()
    record("deduplicate_customers", "Deduplicate the customer list.", True, "approve: 11 clusters", "suryodaya")
    monkeypatch.chdir(tmp_path)
    write_results("suryodaya")
    import json

    raw = (tmp_path / "results.json").read_text()
    body = json.loads(raw)
    assert "tasks" in body
    assert "summary" in body
    row = body["tasks"][0]
    assert "outcome" not in row
    assert row["passed"] is True
    assert isinstance(row["passed"], bool)
    assert '"passed": true' in raw
    assert 0 <= row["score"] <= 1
    assert 1 <= len(body["tasks"]) <= 200


def test_official_task_never_emits_outcome_string():
    from harness.runner import official_task

    row = official_task(
        {"id": "find_and_who_keystone", "title": "who", "outcome": "approve", "detail": "ids match"}
    )
    assert row["passed"] is True
    assert "outcome" not in row


def test_runner_does_not_read_dotenv_passwords():
    src = (ROOT / "harness" / "runner.py").read_text()
    assert "book_password" not in src
    assert "AS_PASSWORD" not in src
    assert "AGENTSWITCH_TOKEN" in src
    assert "AGENTSWITCH_BASE_URL" in src


def test_token_client_skips_login_when_token_set():
    from src.mcp_client import McpClient
    from src.directory_agent import DirectoryAgent

    client = McpClient("https://example.invalid", token="tok")
    assert client.token == "tok"
    agent = DirectoryAgent(client, apply_writes=False)
    assert agent.client.token == "tok"
