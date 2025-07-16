"""Search agent that uses an MCP server to dynamically select and execute tools."""

import asyncio
import json
from typing import Any

import google.generativeai as genai
import mcp
import structlog
from fastmcp import Client
from fastmcp.client.client import CallToolResult

from agents_core.config import config

logger = structlog.get_logger(__name__)

# Configure the Gemini client
genai.configure(api_key=config.gemini.gemini_api_key)


class SearchAgent:
    """Agent that uses Gemini to select and execute tools from an MCP server."""

    def __init__(self, mcp_server_url: str):
        """
        Initializes the SearchAgent.

        Args:
            mcp_server_url: The URL of the MCP server.
        """
        self.mcp_server_url = mcp_server_url
        self.model = genai.GenerativeModel(config.gemini.gemini_model)
        self.mcp_config = {"mcpServers": {"default": {"url": self.mcp_server_url}}}

    async def __call__(self, query: str) -> str:
        """
        Executes the main logic of the agent.

        Args:
            query: The user's query.

        Returns:
            The result from the executed tool as a string.
        """
        logger.info("Agent received query", query=query)
        try:
            async with Client(self.mcp_config) as mcp_client:
                # 1. List available tools
                available_tools = await mcp_client.list_tools()
                if not available_tools:
                    logger.warning("No tools available from MCP server.")
                    return "I'm sorry, but there are no tools available for me to use."

                # 2. Use Gemini to select the best tool
                tool_name, tool_args = await self._select_tool(query, available_tools)
                if not tool_name:
                    logger.warning("Could not select a suitable tool.", query=query)
                    return "I'm sorry, but I couldn't find a suitable tool to answer your query."

                logger.info("Selected tool", tool_name=tool_name, tool_args=tool_args)

                # 3. Call the selected tool
                result: CallToolResult = await mcp_client.call_tool(tool_name, tool_args)

                # 4. Return the result
                if result.is_error:
                    return f"Error calling tool {tool_name}: {result.data}"

                if isinstance(result.structured_content, dict | list):
                    return json.dumps(result.structured_content, indent=2)

                return str(result.structured_content)

        except Exception as e:
            logger.error("An error occurred during agent execution.", exc_info=e)
            return "I'm sorry, but an unexpected error occurred."

    async def _select_tool(
        self, query: str, tools: list[mcp.types.Tool]
    ) -> tuple[str | None, dict[str, Any]]:
        """
        Uses Gemini to select the most appropriate tool for the given query.
        """
        tools_prompt = "\n".join([f"- {tool.name}: {tool.description}" for tool in tools])
        prompt = f"""
You are an intelligent agent that selects the best tool to answer a user's query.
Based on the user's query and the list of available tools, choose the most appropriate tool and determine the arguments to pass to it.

User Query: "{query}"

Available Tools:
{tools_prompt}

Your response must be a JSON object with two keys:
- "tool_name": The name of the selected tool.
- "arguments": An object containing the arguments for the tool. The query should be the primary argument.

Example Response:
{{
  "tool_name": "web_search",
  "arguments": {{
    "query": "latest news on AI"
  }}
}}

Provide only the JSON object in your response.
"""
        try:
            response = await self.model.generate_content_async(prompt)
            cleaned_response = response.text.strip().replace("```json", "").replace("```", "")
            decision = json.loads(cleaned_response)
            return decision.get("tool_name"), decision.get("arguments", {})
        except (json.JSONDecodeError, KeyError, AttributeError) as e:
            logger.error(
                "Failed to parse tool selection response from Gemini.",
                response=response.text,
                error=e,
            )
            return None, {}
        except Exception as e:
            logger.error("An unexpected error occurred during tool selection.", exc_info=e)
            return None, {}


async def main():
    """Example usage of the SearchAgent."""
    # This assumes the MCP server is running at the default location.
    # You can start it from the `agent-tools-mcp` directory.
    agent = SearchAgent(mcp_server_url="http://localhost:8000/mcp/")
    result = await agent("what is the latest news on generative ai?")
    # result = await agent("search for images of cute cats")
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
