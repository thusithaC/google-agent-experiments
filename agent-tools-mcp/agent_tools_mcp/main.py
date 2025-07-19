"""Main module for Brave Search MCP Server."""

from fastmcp import FastMCP

from agent_tools_mcp.code_interpreter import python_interpreter
from agent_tools_mcp.search_tools import (
    image_search,
    news_search,
    video_search,
    web_search,
)
from agent_tools_mcp.settings import settings

# Create the MCP server instance
server = FastMCP("agent-tools-mcp")

# Register tools
server.tool()(python_interpreter)
server.tool()(web_search)
server.tool()(image_search)
server.tool()(video_search)
server.tool()(news_search)


if __name__ == "__main__":
    # For development, run the server directly
    server.run(transport="http", host=settings.server_host, port=settings.server_port, path="/mcp")
