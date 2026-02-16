from typing import Any

from mcp.server.fastmcp import FastMCP

from redmine_mcp.client import RedmineClient

TICKET_RULES_PAGE = "TicketRules"


def register(mcp: FastMCP, client: RedmineClient) -> None:
    """Register wiki-related tools on the MCP server."""

    @mcp.tool()
    async def list_wiki_pages(
        project_id: str,
    ) -> dict[str, Any]:
        """List all wiki pages in a Redmine project.

        Args:
            project_id: Project identifier or numeric id.
        """
        return await client.get(f"/projects/{project_id}/wiki/index.json")

    @mcp.tool()
    async def get_wiki_page(
        project_id: str,
        title: str,
    ) -> dict[str, Any]:
        """Get the content of a specific wiki page.

        Args:
            project_id: Project identifier or numeric id.
            title: Wiki page title (e.g. "Wiki", "TicketRules").
        """
        return await client.get(
            f"/projects/{project_id}/wiki/{title}.json",
        )

    @mcp.tool()
    async def get_ticket_rules(
        project_id: str,
    ) -> dict[str, Any]:
        """Get the ticket creation rules defined in the project wiki.

        Fetches the "TicketRules" wiki page which contains project-specific
        rules for creating issues (required fields, naming conventions,
        description templates, etc.).

        The wiki page follows the convention defined in docs/wiki-convention.md.
        If the page does not exist, a 404 error is returned — meaning the
        project has no specific ticket creation rules.

        Args:
            project_id: Project identifier or numeric id.
        """
        return await client.get(
            f"/projects/{project_id}/wiki/{TICKET_RULES_PAGE}.json",
        )
