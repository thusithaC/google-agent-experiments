from fastmcp import Client
import mcp


# Standard MCP configuration with multiple servers
config = {
    "mcpServers": {
        "search": {"url": "http://localhost:8000/mcp/"},
    }
}

# Create a client that connects to all servers
client = Client(config)


async def main():
    # Connect via in-memory transport
    async with client:
        tools: list[mcp.types.Tool] = await client.list_tools()
        print(f"Available tools: {tools}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())