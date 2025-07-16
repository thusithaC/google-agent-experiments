#!/bin/bash
set -euo pipefail
echo "Starting Agent Tools MCP Server with uvicorn..."
echo "Server will be available at: http://0.0.0.0:8000/mcp"
echo "Press Ctrl+C to stop the server"

# Run the MCP server using uvicorn
uv run python agent_tools_mcp/main.py
