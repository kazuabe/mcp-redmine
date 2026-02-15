import pytest

from redmine_mcp.server import mcp


@pytest.mark.asyncio
async def test_tools_registered():
    """Verify that all expected tools are registered."""
    tool_names = set(mcp._tool_manager._tools.keys())
    expected = {
        "list_issues", "get_issue", "search_issues",
        "create_issue", "update_issue", "add_comment",
        "bulk_update_issues",
        "list_projects", "get_project",
        "list_statuses", "list_trackers", "list_priorities", "list_users",
    }
    assert expected.issubset(tool_names), f"Missing tools: {expected - tool_names}"
