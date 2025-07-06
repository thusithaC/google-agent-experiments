#!/bin/bash
"""Run the Brave Search MCP Server with SSE transport."""

echo "Starting Brave Search MCP Server with SSE transport..."
echo "Server will be available at: http://0.0.0.0:8000/sse"
echo "Press Ctrl+C to stop the server"

# Run the MCP server directly using Python with uv
uv run python -m brave_search_mcp.main
