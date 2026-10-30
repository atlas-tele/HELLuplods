import asyncio

import pytest

from app.agents.base import NotImplementedYet, run_agent
from app.agents.registry import AGENTS, IMPLEMENTATIONS
from app.services.ssrf import UnsafeURL, validate_public_url
from app.services.storage import LocalStorage


@pytest.mark.parametrize("url", [
    "http://127.0.0.1/", "http://10.0.0.5/", "http://169.254.169.254/", "http://localhost/",
    "http://[::1]/", "file:///etc/passwd", "ftp://example.com", "http://u:p@example.com/",
    "http://[::ffff:127.0.0.1]/",
])
def test_ssrf_blocks(url):
    with pytest.raises(UnsafeURL):
        validate_public_url(url, resolve=False)


def test_ssrf_allows_public_ip():
    assert validate_public_url("https://8.8.8.8/", resolve=False)


def test_storage_blocks_traversal(tmp_path):
    store = LocalStorage(str(tmp_path))
    for bad in ["../x", "/etc/passwd", "a/../../x", ""]:
        with pytest.raises(ValueError):
            store.put(bad, b"x")
    meta = store.put("shots/a.png", b"data")
    assert store.get("shots/a.png") == b"data" and meta["size_bytes"] == 4


def test_all_sixteen_agents_defined_with_limits():
    assert len(AGENTS) == 16
    for spec in AGENTS.values():
        assert spec.timeout_seconds > 0 and spec.max_retries >= 0


def test_unbuilt_agent_reports_not_implemented():
    spec = AGENTS["research"]
    result = asyncio.run(run_agent(spec, IMPLEMENTATIONS["research"], {"project_id": "p", "target": "x"}))
    assert result.status == "not_implemented"


def test_agent_cannot_use_unlisted_tool_or_secret():
    from app.agents.base import PermissionDenied, ToolBox
    box = ToolBox(AGENTS["screenshot"], {"shell": print}, {"ANTHROPIC_API_KEY": "k"})
    with pytest.raises(PermissionDenied):
        box.tool("shell")
    with pytest.raises(PermissionDenied):
        box.secret("ANTHROPIC_API_KEY")
