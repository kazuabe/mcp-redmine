from typing import Any

from mcp.server.fastmcp import FastMCP

from redmine_mcp.client import RedmineClient


def register(mcp: FastMCP, client: RedmineClient) -> None:
    """Register issue-related tools on the MCP server."""

    @mcp.tool()
    async def list_issues(
        project_id: str | None = None,
        status_id: str | None = None,
        assigned_to_id: str | None = None,
        tracker_id: int | None = None,
        limit: int = 25,
        offset: int = 0,
        sort: str | None = None,
    ) -> dict[str, Any]:
        """List Redmine issues with optional filters.

        Args:
            project_id: Filter by project identifier or id.
            status_id: Filter by status id. Use "open", "closed", "*" or a numeric id.
            assigned_to_id: Filter by assignee id. Use "me" for current user.
            tracker_id: Filter by tracker id.
            limit: Max number of issues to return (default 25, max 100).
            offset: Number of issues to skip.
            sort: Sort field and direction, e.g. "updated_on:desc".
        """
        params: dict[str, Any] = {"limit": limit, "offset": offset}
        if project_id is not None:
            params["project_id"] = project_id
        if status_id is not None:
            params["status_id"] = status_id
        if assigned_to_id is not None:
            params["assigned_to_id"] = assigned_to_id
        if tracker_id is not None:
            params["tracker_id"] = tracker_id
        if sort is not None:
            params["sort"] = sort
        return await client.get("/issues.json", params=params)

    @mcp.tool()
    async def get_issue(
        issue_id: int,
        include: str | None = None,
    ) -> dict[str, Any]:
        """Get detailed information about a specific Redmine issue.

        Args:
            issue_id: The issue id.
            include: Comma-separated list of associations to include:
                     journals, children, attachments, relations, changesets, watchers.
        """
        params: dict[str, Any] = {}
        if include is not None:
            params["include"] = include
        return await client.get(f"/issues/{issue_id}.json", params=params)

    @mcp.tool()
    async def search_issues(
        query: str,
        project_id: str | None = None,
        limit: int = 25,
        offset: int = 0,
    ) -> dict[str, Any]:
        """Search Redmine issues by keyword.

        Args:
            query: Search keyword.
            project_id: Limit search to a project.
            limit: Max results.
            offset: Skip results.
        """
        params: dict[str, Any] = {
            "q": query,
            "issues": 1,
            "limit": limit,
            "offset": offset,
        }
        if project_id is not None:
            params["project_id"] = project_id
        return await client.get("/search.json", params=params)

    @mcp.tool()
    async def create_issue(
        project_id: str,
        subject: str,
        description: str | None = None,
        tracker_id: int | None = None,
        status_id: int | None = None,
        priority_id: int | None = None,
        assigned_to_id: int | None = None,
        parent_issue_id: int | None = None,
        start_date: str | None = None,
        due_date: str | None = None,
        estimated_hours: float | None = None,
    ) -> dict[str, Any]:
        """Create a new Redmine issue.

        Args:
            project_id: Project identifier or id (required).
            subject: Issue subject (required).
            description: Issue description (Textile or Markdown depending on Redmine config).
            tracker_id: Tracker id.
            status_id: Status id.
            priority_id: Priority id.
            assigned_to_id: Assignee user id.
            parent_issue_id: Parent issue id.
            start_date: Start date (YYYY-MM-DD).
            due_date: Due date (YYYY-MM-DD).
            estimated_hours: Estimated hours.
        """
        issue_data: dict[str, Any] = {
            "project_id": project_id,
            "subject": subject,
        }
        for key in (
            "description", "tracker_id", "status_id", "priority_id",
            "assigned_to_id", "parent_issue_id", "start_date", "due_date",
            "estimated_hours",
        ):
            val = locals()[key]
            if val is not None:
                issue_data[key] = val
        return await client.post("/issues.json", json={"issue": issue_data})

    @mcp.tool()
    async def update_issue(
        issue_id: int,
        subject: str | None = None,
        description: str | None = None,
        status_id: int | None = None,
        priority_id: int | None = None,
        assigned_to_id: int | None = None,
        tracker_id: int | None = None,
        notes: str | None = None,
        private_notes: bool = False,
        start_date: str | None = None,
        due_date: str | None = None,
        estimated_hours: float | None = None,
        done_ratio: int | None = None,
    ) -> dict[str, Any]:
        """Update an existing Redmine issue.

        Args:
            issue_id: The issue id to update (required).
            subject: New subject.
            description: New description.
            status_id: New status id.
            priority_id: New priority id.
            assigned_to_id: New assignee user id.
            tracker_id: New tracker id.
            notes: Comment to add with the update.
            private_notes: Whether the notes are private.
            start_date: New start date (YYYY-MM-DD).
            due_date: New due date (YYYY-MM-DD).
            estimated_hours: New estimated hours.
            done_ratio: Percentage done (0-100).
        """
        issue_data: dict[str, Any] = {}
        for key in (
            "subject", "description", "status_id", "priority_id",
            "assigned_to_id", "tracker_id", "notes", "start_date",
            "due_date", "estimated_hours", "done_ratio",
        ):
            val = locals()[key]
            if val is not None:
                issue_data[key] = val
        if private_notes and notes:
            issue_data["private_notes"] = True
        return await client.put(f"/issues/{issue_id}.json", json={"issue": issue_data})

    @mcp.tool()
    async def add_comment(
        issue_id: int,
        notes: str,
        private_notes: bool = False,
    ) -> dict[str, Any]:
        """Add a comment (journal note) to a Redmine issue.

        Args:
            issue_id: The issue id.
            notes: Comment text.
            private_notes: Whether the comment is private.
        """
        issue_data: dict[str, Any] = {"notes": notes}
        if private_notes:
            issue_data["private_notes"] = True
        return await client.put(f"/issues/{issue_id}.json", json={"issue": issue_data})

    @mcp.tool()
    async def bulk_update_issues(
        issue_ids: list[int],
        status_id: int | None = None,
        priority_id: int | None = None,
        assigned_to_id: int | None = None,
        notes: str | None = None,
    ) -> dict[str, Any]:
        """Update multiple Redmine issues at once.

        Args:
            issue_ids: List of issue ids to update.
            status_id: New status id for all issues.
            priority_id: New priority id for all issues.
            assigned_to_id: New assignee for all issues.
            notes: Comment to add to all issues.
        """
        issue_data: dict[str, Any] = {}
        if status_id is not None:
            issue_data["status_id"] = status_id
        if priority_id is not None:
            issue_data["priority_id"] = priority_id
        if assigned_to_id is not None:
            issue_data["assigned_to_id"] = assigned_to_id
        if notes is not None:
            issue_data["notes"] = notes

        results = []
        for iid in issue_ids:
            try:
                await client.put(f"/issues/{iid}.json", json={"issue": issue_data})
                results.append({"id": iid, "status": "ok"})
            except Exception as e:
                results.append({"id": iid, "status": "error", "message": str(e)})
        return {"results": results}
