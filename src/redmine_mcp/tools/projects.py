from typing import Any

from mcp.server.fastmcp import FastMCP

from redmine_mcp.client import RedmineClient


def register(mcp: FastMCP, client: RedmineClient) -> None:
    """Register project-related tools on the MCP server."""

    @mcp.tool()
    async def list_projects(
        limit: int = 25,
        offset: int = 0,
    ) -> dict[str, Any]:
        """List all accessible Redmine projects.

        Args:
            limit: Max number of projects to return.
            offset: Number of projects to skip.
        """
        return await client.get("/projects.json", params={"limit": limit, "offset": offset})

    @mcp.tool()
    async def get_project(
        project_id: str,
        include: str | None = None,
    ) -> dict[str, Any]:
        """Get detailed information about a Redmine project.

        Args:
            project_id: Project identifier or numeric id.
            include: Comma-separated associations: trackers, issue_categories, enabled_modules, time_entry_activities.
        """
        params: dict[str, Any] = {}
        if include is not None:
            params["include"] = include
        return await client.get(f"/projects/{project_id}.json", params=params)
