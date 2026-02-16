from unittest.mock import AsyncMock, patch

import pytest

from redmine_mcp.tools.wiki import TICKET_RULES_PAGE


@pytest.fixture
def mock_client():
    from redmine_mcp.client import RedmineClient

    with patch.object(RedmineClient, "__init__", lambda self, **kw: None):
        client = RedmineClient()
        client.get = AsyncMock()
        return client


@pytest.mark.asyncio
async def test_list_wiki_pages(mock_client):
    from mcp.server.fastmcp import FastMCP

    from redmine_mcp.tools import wiki

    mcp = FastMCP("test")
    wiki.register(mcp, mock_client)

    mock_client.get.return_value = {
        "wiki_pages": [
            {"title": "Wiki"},
            {"title": "TicketRules"},
        ]
    }

    tool_fn = mcp._tool_manager._tools["list_wiki_pages"].fn
    result = await tool_fn(project_id="myproject")

    mock_client.get.assert_called_once_with("/projects/myproject/wiki/index.json")
    assert len(result["wiki_pages"]) == 2


@pytest.mark.asyncio
async def test_get_wiki_page(mock_client):
    from mcp.server.fastmcp import FastMCP

    from redmine_mcp.tools import wiki

    mcp = FastMCP("test")
    wiki.register(mcp, mock_client)

    mock_client.get.return_value = {
        "wiki_page": {
            "title": "Guide",
            "text": "# Guide\nSome content",
            "version": 3,
        }
    }

    tool_fn = mcp._tool_manager._tools["get_wiki_page"].fn
    result = await tool_fn(project_id="myproject", title="Guide")

    mock_client.get.assert_called_once_with("/projects/myproject/wiki/Guide.json")
    assert result["wiki_page"]["title"] == "Guide"


@pytest.mark.asyncio
async def test_get_ticket_rules(mock_client):
    from mcp.server.fastmcp import FastMCP

    from redmine_mcp.tools import wiki

    mcp = FastMCP("test")
    wiki.register(mcp, mock_client)

    mock_client.get.return_value = {
        "wiki_page": {
            "title": TICKET_RULES_PAGE,
            "text": "# TicketRules\n## 必須フィールド\n- subject\n- tracker_id",
            "version": 1,
        }
    }

    tool_fn = mcp._tool_manager._tools["get_ticket_rules"].fn
    result = await tool_fn(project_id="myproject")

    mock_client.get.assert_called_once_with(
        f"/projects/myproject/wiki/{TICKET_RULES_PAGE}.json"
    )
    assert result["wiki_page"]["title"] == TICKET_RULES_PAGE
