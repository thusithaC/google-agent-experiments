import asyncio
import sys

from agents_core.search_agent import SearchAgent


async def main():
    if len(sys.argv) < 2:
        print("Usage: python cli_search_example.py <your query>")
        sys.exit(1)

    query = " ".join(sys.argv[1:])
    agent = SearchAgent()
    response = await agent.process_message(query)
    print("Agent response:")
    print(response)


if __name__ == "__main__":
    asyncio.run(main())
