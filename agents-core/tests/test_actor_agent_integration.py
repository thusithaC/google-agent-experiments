"""Integration tests for the Actor agent."""

import json
from unittest.mock import AsyncMock, MagicMock

import mcp.types
import pytest
from fastmcp import Client
from fastmcp.client.client import CallToolResult

from agents_core.actor_agent import ActorAgent


@pytest.fixture
def mock_mcp_client():
    """Fixture for a mocked MCP client."""
    client = MagicMock(spec=Client)
    client.list_tools = AsyncMock(
        # return should be list of [mcp.types.Tool] objects
        return_value=[
            mcp.types.Tool(
                name="web_search",
                description="Search the web",
                inputSchema={"query": {"type": "string"}},
            ),
        ]
    )

    # Mock the return value of call_tool to be a CallToolResult instance
    tool_result = CallToolResult(
        content=[mcp.types.TextContent(type="text", text="some search result")],
        structured_content={"result": "some search result"},
        is_error=False,
    )
    client.call_tool = AsyncMock(return_value=tool_result)

    # Mock the async context manager
    client.__aenter__ = AsyncMock(return_value=client)
    client.__aexit__ = AsyncMock(return_value=None)
    return client


@pytest.mark.asyncio
async def test_actor_agent_tool_call(mock_mcp_client):
    """Test that the ActorAgent can parse a tool call and execute it."""

    # Instantiate the agent. It will receive the mocked client.
    agent = ActorAgent()

    # Mock the model's response to be a valid tool call in the expected JSON format
    tool_call_response = {
        "tool_name": "web_search",
        "parameters": {"query": "test"},
    }
    mock_model_response = MagicMock()
    mock_model_response.text = json.dumps(tool_call_response)

    # Patch the agent's model to return the mocked response
    agent.model.generate_content = AsyncMock(return_value=mock_model_response)

    # patch the agent's mcp client to use the mock client
    agent.mcp_client = mock_mcp_client

    # Process a message that should trigger the tool call
    response = await agent.process_message("Search for 'test'")

    # Assert that the mcp_client.call_tool method was called with the correct arguments
    mock_mcp_client.call_tool.assert_called_once_with("web_search", arguments={"query": "test"})

    # Assert that the final response is the stringified result of the tool call
    expected = (
        '{"tool_name": "web_search", "parameters": {"query": "test"}}\n'
        'Tool result: [{"type": "text", "text": "some search result", "annotations": null, "meta": null}]'
    )
    assert response == expected
