from typing import Any

from mcp.server.fastmcp import FastMCP

from redmine_mcp.client import RedmineClient


def register(mcp: FastMCP, client: RedmineClient) -> None:
    """Register master data reference tools on the MCP server."""

    @mcp.tool()
    async def list_statuses() -> dict[str, Any]:
        """List all issue statuses available in Redmine."""
        return await client.get("/issue_statuses.json")

    @mcp.tool()
    async def list_trackers() -> dict[str, Any]:
        """List all trackers available in Redmine."""
        return await client.get("/trackers.json")

    @mcp.tool()
    async def list_priorities() -> dict[str, Any]:
        """List all issue priorities available in Redmine."""
        return await client.get("/enumerations/issue_priorities.json")

    @mcp.tool()
    async def list_users(
        status: int | None = None,
        name: str | None = None,
        limit: int = 25,
        offset: int = 0,
    ) -> dict[str, Any]:
        """List Redmine users (requires admin privileges).

        Args:
            status: Filter by user status (0=anonymous, 1=active, 2=registered, 3=locked).
            name: Filter by name or login (partial match).
            limit: Max number of users to return.
            offset: Number of users to skip.
        """
        params: dict[str, Any] = {"limit": limit, "offset": offset}
        if status is not None:
            params["status"] = status
        if name is not None:
            params["name"] = name
        return await client.get("/users.json", params=params)
