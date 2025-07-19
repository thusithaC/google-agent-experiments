"""Actor agent that interacts with tools to accomplish a task."""

import json
from typing import Any

import mcp
import structlog
from fastmcp import Client

from agents_core.base_agent import BaseAgent

logger = structlog.get_logger(__name__)


class ActorAgent(BaseAgent):
    """Actor agent that interacts with tools to accomplish a task."""

    def __init__(
        self,
        name: str = "Actor",
        model_name: str | None = None,
        mcp_server_url: str = "http://localhost:8000/mcp/",
    ):
        super().__init__(name, model_name)
        self.mcp_server_url = mcp_server_url
        self.mcp_client = Client({"mcpServers": {"default": {"url": self.mcp_server_url}}})

    async def get_system_prompt(self) -> str:
        return (
            "You are an actor agent. Your goal is to accomplish the given task by using the available tools. "
            "When you need to use a tool, respond with a JSON object with two keys: "
            '"tool_name" (the name of the tool to call) and "parameters" (an object of arguments to pass to the tool). '
            "Otherwise, respond with your thoughts."
        )

    async def get_available_tools(self) -> list[dict[str, any]]:
        """Get list of tools available to this agent."""
        async with self.mcp_client as client:
            tools: list[mcp.types.Tool] = await client.list_tools()
            return [tool.model_dump() for tool in tools]

    async def process_message(self, message: str, context: dict[str, Any] | None = None) -> str:
        """Process a user message, execute tool calls, and return a response."""
        # Add user message to history
        self.conversation_history.append({"role": "user", "content": message})

        # Get system prompt and available tools
        system_prompt = await self.get_system_prompt()
        tools = await self.get_available_tools()
        # We will inject the tools into the context for the model
        context = context or {}
        context["available_tools"] = tools

        # Prepare the conversation for Gemini
        conversation_text = self._format_conversation_for_gemini(system_prompt)

        # Generate response from the model
        raw_response = await self._generate_response(conversation_text, context)

        self.conversation_history.append({"role": "assistant", "content": raw_response})
        # Check if the response is a tool call
        try:
            tool_call = json.loads(raw_response)
            if "tool_name" in tool_call and "parameters" in tool_call:
                tool_name = tool_call["tool_name"]
                parameters = tool_call["parameters"]

                # Execute the tool call
                async with self.mcp_client as client:
                    tool_result = await client.call_tool(tool_name, arguments=parameters)

                # Add tool call and result to history
                if tool_result.content:
                    # we iterate over the content and convert the pydantic model to json before appending.
                    tool_result = [item.model_dump() for item in tool_result.content]
                    self.conversation_history.append(
                        {"role": "user", "content": f"Tool result: {json.dumps(tool_result)}"}
                    )
                    raw_response += f"\nTool result: {json.dumps(tool_result)}"
                else:
                    self.conversation_history.append(
                        {"role": "user", "content": "Tool result error"}
                    )
                    raw_response += "\nTool result: error"
        except (json.JSONDecodeError, KeyError):
            # Not a valid tool call, treat as a regular message
            logger.warning(
                "Received response that is not a valid tool call.",
                response=raw_response,
            )
            self.conversation_history.append({"role": "user", "content": "Tool result error"})
            raw_response += "\nTool result: error"
        return raw_response
