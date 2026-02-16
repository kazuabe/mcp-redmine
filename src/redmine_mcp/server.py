from mcp.server.fastmcp import FastMCP

from redmine_mcp.client import RedmineClient
from redmine_mcp.tools import issues, master, projects, wiki

mcp = FastMCP("redmine")
client = RedmineClient()

issues.register(mcp, client)
projects.register(mcp, client)
master.register(mcp, client)
wiki.register(mcp, client)
