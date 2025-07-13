#!/bin/bash
"""Run the Brave Search MCP Server with uvicorn."""

echo "Starting Brave Search MCP Server with uvicorn..."
echo "Server will be available at: http://0.0.0.0:8000/mcp"
echo "Press Ctrl+C to stop the server"

# Run the MCP server using uvicorn
uvicorn brave_search_mcp.main:app --host 0.0.0.0 --port 8000
