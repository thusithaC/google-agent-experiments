import asyncio

import click
import mcp
from fastmcp import Client

from agents_core.search_agent import SearchAgent


@click.group()
def cli():
    """A CLI for interacting with the MCP server."""
    pass


@cli.command()
@click.option("--url", default="http://localhost:8000/mcp/", help="The URL of the MCP server.")
def list_tools(url):
    """Lists the available tools on the MCP server."""
    config = {
        "mcpServers": {
            "default": {"url": url},
        }
    }
    client = Client(config)

    async def _list_tools():
        async with client:
            tools: list[mcp.types.Tool] = await client.list_tools()
            for tool in tools:
                click.echo(f"- {tool.name}: {tool.description}")

    asyncio.run(_list_tools())


@cli.command()
@click.argument("question")
@click.option("--url", default="http://localhost:8000/mcp/", help="The URL of the MCP server.")
def search_agent(question, url):
    """Runs the search agent with a given question."""

    async def _search_agent():
        agent = SearchAgent(mcp_server_url=url)
        result = await agent(question)
        click.echo(result)

    asyncio.run(_search_agent())


if __name__ == "__main__":
    cli()
