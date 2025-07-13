# MCP Search Agent Integration

This implementation integrates your local MCP server for web search with Google's Gemini using a clean agent architecture.

## Architecture Overview

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   SearchAgent   │    │    MCPClient     │    │  Local MCP      │
│   (Gemini AI)   │◄──►│  (HTTP Client)   │◄──►│    Server       │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## Key Components

### 1. **MCPClient** (`mcp_client.py`)
- Handles communication with your MCP server at `localhost:8000/mcp`
- Implements JSON-RPC 2.0 protocol for MCP
- Provides methods for tool discovery and execution
- Async context manager for connection lifecycle

### 2. **BaseAgent** (`base_agent.py`)
- Abstract base class for all agents
- Integrates with Google Gemini for AI capabilities
- Manages conversation history
- Provides template methods for customization

### 3. **SearchAgent** (`search_agent.py`)
- Specialized agent for web search tasks
- Automatically determines when web search is needed
- Synthesizes search results using Gemini
- Provides comprehensive responses with source citations

### 4. **Configuration** (`config.py`)
- Pydantic-based configuration management
- Environment variable support with nested structure
- Type-safe configuration with defaults

## Setup

1. **Install dependencies:**
   ```bash
   cd agents-core
   uv sync
   ```

2. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env and add your Gemini API key
   ```

3. **Ensure your MCP server is running:**
   ```bash
   # Your MCP server should be accessible at localhost:8000/mcp
   curl http://localhost:8000/mcp/tools/list
   ```

## Usage

### Basic Usage

```python
import asyncio
from agents_core import SearchAgent

async def main():
    # Create a search agent
    agent = SearchAgent("MySearchBot")
    
    # Ask a question that requires web search
    response = await agent.process_message(
        "What are the latest developments in AI?"
    )
    print(response)

asyncio.run(main())
```

### Direct Search

```python
import asyncio
from agents_core import SearchAgent

async def main():
    agent = SearchAgent()
    
    # Perform direct search and get synthesized response
    response = await agent.search_and_respond(
        "latest AI news", 
        max_results=5
    )
    print(response)

asyncio.run(main())
```

### Using MCP Client Directly

```python
import asyncio
from agents_core import MCPClient

async def main():
    async with MCPClient() as client:
        # List available tools
        tools = await client.list_tools()
        print("Available tools:", tools)
        
        # Perform search
        results = await client.search_web("AI news")
        print("Search results:", results)

asyncio.run(main())
```

## Configuration

The system uses environment variables with the `AGENT_` prefix:

```bash
# Required
AGENT_GEMINI__API_KEY=your-api-key

# MCP Server (optional)
AGENT_MCP__HOST=localhost
AGENT_MCP__PORT=8000
AGENT_MCP__PATH=/mcp

# Gemini Settings (optional)
AGENT_GEMINI__MODEL=gemini-1.5-flash
AGENT_GEMINI__TEMPERATURE=0.1
```

## Example Run

```bash
# Set your API key
export AGENT_GEMINI__API_KEY="your-gemini-api-key"

## MCP Server Requirements

Your MCP server should implement:

1. **Initialization endpoint:** `POST /mcp/initialize`
2. **Tool listing:** `POST /mcp/tools/list`
3. **Tool execution:** `POST /mcp/tools/call`

Expected tool format for web search:
```json
{
  "name": "web_search",
  "parameters": {
    "query": "search terms",
    "max_results": 5
  }
}
```

## How It Works

1. **Message Processing:** When you send a message to SearchAgent, it first uses Gemini to determine if web search is needed.

2. **Query Extraction:** If search is needed, Gemini extracts the optimal search query from your message.

3. **MCP Search:** The MCPClient calls your local MCP server's web search tool.

4. **Result Synthesis:** Gemini analyzes the search results and creates a comprehensive response with source citations.

5. **Response:** You get a well-formatted answer that combines information from multiple sources.

## Extending the System

### Creating Custom Agents

```python
from agents_core import BaseAgent

class MyCustomAgent(BaseAgent):
    async def get_system_prompt(self) -> str:
        return "You are a helpful assistant that..."
    
    async def get_available_tools(self) -> List[Dict[str, Any]]:
        return [...]  # Define your tools
```

### Adding New MCP Tools

```python
# In your SearchAgent or custom agent
async def call_custom_tool(self, tool_name: str, params: dict):
    async with MCPClient() as client:
        return await client.call_tool(tool_name, params)
```

This architecture provides a solid foundation for building AI agents that can leverage your MCP server's capabilities while using Google's Gemini for intelligent processing and response generation.
