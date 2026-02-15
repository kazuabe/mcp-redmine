# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

An MCP (Model Context Protocol) server that exposes Redmine REST API operations as tools. It allows coding agents like Claude Code to read and write Redmine issues, projects, and master data via stdio transport.

## Commands

```bash
# Install dependencies
uv sync

# Run tests (requires env vars since server module imports RedmineClient at module level)
REDMINE_URL=https://redmine.example.com REDMINE_API_KEY=test-key uv run pytest tests/ -v

# Run a single test
REDMINE_URL=https://redmine.example.com REDMINE_API_KEY=test-key uv run pytest tests/test_client.py::test_get -v

# Start the MCP server
REDMINE_URL=https://your-redmine.example.com REDMINE_API_KEY=your-key uv run python main.py

# Test with MCP Inspector
REDMINE_URL=https://your-redmine.example.com REDMINE_API_KEY=your-key mcp dev main.py
```

## Architecture

**Entry point**: `main.py` imports the FastMCP instance from `server.py` and runs it with stdio transport.

**Server assembly** (`src/redmine_mcp/server.py`): Creates the FastMCP instance and a single `RedmineClient`, then calls `register(mcp, client)` on each tool module. This is where all wiring happens.

**API client** (`src/redmine_mcp/client.py`): `RedmineClient` wraps httpx with async `get/post/put/delete` methods. Reads `REDMINE_URL` and `REDMINE_API_KEY` from env vars at construction time. Adds `X-Redmine-API-Key` header automatically.

**Tool modules** (`src/redmine_mcp/tools/`): Each module exports a `register(mcp, client)` function that defines `@mcp.tool()` decorated async functions as closures over the shared client. Three modules:
- `issues.py` — list, get, search, create, update, comment, bulk update
- `projects.py` — list, get
- `master.py` — statuses, trackers, priorities, users

### Adding a new tool

1. Add an async function decorated with `@mcp.tool()` inside the `register()` function of the appropriate tool module
2. The function receives the shared `RedmineClient` via closure
3. If creating a new tool module, add a `register()` function and call it from `server.py`

## Configuration

Environment variables (required at startup):
- `REDMINE_URL` — Base URL of the Redmine instance
- `REDMINE_API_KEY` — API key for authentication
