"""Search agent that uses MCP server for web search capabilities."""

import json
from typing import Any

import structlog

from agents_core.base_agent import BaseAgent

logger = structlog.get_logger(__name__)


class SearchAgent(BaseAgent):
    """Agent that can perform web searches using an MCP server."""

    def __init__(self, name: str = "SearchAgent", model_name: str | None = None):
        """Initialize the search agent.

        Args:
            name: Name of the agent
            model_name: Gemini model to use
        """
        super().__init__(name, model_name)
        self.mcp_client = None  # Placeholder for MCP client, initialized in perform_web_search

    async def get_system_prompt(self) -> str:
        """Get the system prompt for the search agent."""
        return """You are a helpful search agent with access to web search capabilities.

Your role is to:
1. Help users find information by searching the web
2. Provide accurate, up-to-date information from reliable sources
3. Summarize search results in a clear and helpful way
4. Cite sources when providing information

When a user asks a question that requires current information or web search:
1. Use the web search tool to find relevant information
2. Analyze the search results
3. Provide a comprehensive answer based on the findings
4. Include relevant links and sources

Be helpful, accurate, and cite your sources. If you cannot find reliable information, say so clearly."""

    async def get_available_tools(self) -> list[dict[str, Any]]:
        """Get list of tools available to the search agent."""
        # TODO
        # call the MCP server to get the list of available tools


    async def search_and_respond(self, query: str, max_results: int = 5) -> str:
        """Search the web and provide a comprehensive response.

        Args:
            query: Search query
            max_results: Maximum number of results to return

        Returns:
            Comprehensive response based on search results
        """
        try:
            # Perform the search
            search_results = await self.perform_web_search(query, max_results)

            # Create a prompt for Gemini to analyze the search results
            analysis_prompt = f"""Based on the following search results for the query "{query}", provide a comprehensive and helpful response:

Search Results:
{json.dumps(search_results, indent=2)}

Please:
1. Synthesize the information from multiple sources
2. Provide a clear and informative answer
3. Include relevant details and context
4. Cite specific sources when possible
5. If there are conflicting information, mention it

Response:"""

            # Generate response using Gemini
            response = self.model.generate_content(analysis_prompt)

            logger.info(
                "Search and response completed", query=query, result_count=len(search_results)
            )
            return response.text

        except Exception as e:
            logger.error("Search and response failed", query=query, error=str(e))
            return f"I apologize, but I encountered an error while searching for information about '{query}'. Please try again or rephrase your question."

    async def perform_web_search(self, query: str, max_results: int = 5) -> list[dict[str, Any]]:
        """Perform a web search using the MCP server.

        Args:
            query: Search query
            max_results: Maximum number of results

        Returns:
            List of search results
        """
        try:
            async with MCPClient() as mcp_client:
                search_results = await mcp_client.search_web(query, max_results)
                return search_results

        except Exception as e:
            logger.error("Web search failed", query=query, error=str(e))
            raise

    async def process_message(self, message: str, context: dict[str, Any] | None = None) -> str:
        """Process a user message, determining if web search is needed.

        Args:
            message: User message
            context: Optional context information

        Returns:
            Agent response
        """
        try:
            # First, determine if the message requires a web search
            search_decision_prompt = f"""Analyze this user message and determine if it requires a web search to provide an accurate answer:

User message: "{message}"

Consider:
- Does the question require current/recent information?
- Is it asking about specific facts, news, or data?
- Would a web search provide better, more accurate information?

Respond with only "YES" if a web search is needed, or "NO" if you can answer without searching.

Decision:"""

            decision_response = self.model.generate_content(search_decision_prompt)
            needs_search = "YES" in decision_response.text.upper()

            if needs_search:
                # Extract search query
                query_prompt = f"""Extract the best search query from this user message to find relevant information:

User message: "{message}"

Provide only the search query, nothing else:"""

                query_response = self.model.generate_content(query_prompt)
                search_query = query_response.text.strip()

                # Perform search and respond
                return await self.search_and_respond(search_query)
            else:
                # Use normal processing without search
                return await super().process_message(message, context)

        except Exception as e:
            logger.error("Message processing failed", error=str(e))
            return await super().process_message(message, context)

    async def get_search_suggestions(self, topic: str) -> list[str]:
        """Get search suggestions for a given topic.

        Args:
            topic: Topic to get suggestions for

        Returns:
            List of suggested search queries
        """
        suggestions_prompt = f"""Generate 5 helpful search queries related to the topic: "{topic}"

The queries should be:
- Specific and focused
- Likely to return useful results
- Varied in scope (broad to specific)

Provide only the queries, one per line:"""

        response = self.model.generate_content(suggestions_prompt)
        suggestions = [line.strip() for line in response.text.split("\n") if line.strip()]

        return suggestions[:5]  # Ensure we return at most 5 suggestions
