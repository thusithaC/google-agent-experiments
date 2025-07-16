# Agent Tools MCP Server

A Model Context Protocol (MCP) server that provides access to various tools. Currently, it supports the Brave Search API capabilities including web search, image search, video search, and news search.

## Features

- **Web Search**: Search the web with advanced filtering options
- **Image Search**: Find images with detailed metadata
- **Video Search**: Search for videos with duration and view counts
- **News Search**: Get the latest news articles
- **HTTP API**: Exposed as a FastAPI/uvicorn HTTP server
- **OpenAPI Documentation**: Auto-generated API docs

## Installation

1. Install dependencies:
```bash
pip install -e .
```

2. Set up your Brave Search API key in `.env`:
```bash
BRAVE_SEARCH_API_KEY=your_api_key_here
```

Optional environment variables:
```bash
SERVER_HOST=0.0.0.0        # Default: 0.0.0.0
SERVER_PORT=8000           # Default: 8000
LOG_LEVEL=info             # Default: info
```

## Configuration

The server uses Pydantic Settings for configuration management. Settings are automatically loaded from:
1. Environment variables
2. `.env` file in the project root
3. Default values

### Required Settings
- `BRAVE_SEARCH_API_KEY`: Your Brave Search API key (required)

### Optional Settings
- `SERVER_HOST`: Server host address (default: 0.0.0.0)
- `SERVER_PORT`: Server port number (default: 8000)  
- `LOG_LEVEL`: Logging level (default: info)

## Running the Server

### Using the main module:
```bash
python -m agent_tools_mcp.main
```

### Using the run script:
```bash
python run_server.py
```

### Using uvicorn directly:
```bash
uvicorn agent_tools_mcp.main:server --host 0.0.0.0 --port 8000 --reload
```

The server will be available at:
- **API**: http://localhost:8000
- **Documentation**: http://localhost:8000/docs
- **OpenAPI Schema**: http://localhost:8000/openapi.json

## API Endpoints

### Web Search
`POST /tools/web_search`
- Search the web with optional country, language, and filtering parameters
- Returns structured JSON with titles, URLs, descriptions, and metadata

### Image Search  
`POST /tools/image_search`
- Search for images with thumbnail and metadata
- Returns image URLs, dimensions, format, and source information

### Video Search
`POST /tools/video_search`  
- Search for videos with duration and view information
- Returns video URLs, thumbnails, descriptions, and statistics

### News Search
`POST /tools/news_search`
- Search for recent news articles
- Returns article titles, URLs, sources, and publication dates

## Tool Parameters

### web_search
- `query` (required): Search query string
- `count` (optional): Number of results (1-20, default: 10)
- `country` (optional): Country code (e.g., 'US', 'DE', 'FR')
- `search_lang` (optional): Language code (e.g., 'en', 'de', 'fr')
- `safe_search` (optional): Safety filter ('strict', 'moderate', 'off')
- `freshness` (optional): Time filter ('pd', 'pw', 'pm', 'py')

### image_search, video_search, news_search
- `query` (required): Search query string  
- `count` (optional): Number of results (1-20, default: 10)

## Example Usage

Using curl:
```bash
# Web search
curl -X POST "http://localhost:8000/tools/web_search" \
  -H "Content-Type: application/json" \
  -d '{"query": "python programming", "count": 5}'

# Image search
curl -X POST "http://localhost:8000/tools/image_search" \
  -H "Content-Type: application/json" \
  -d '{"query": "cats", "count": 3}'
```

## Development

Install in development mode:
```bash
pip install -e ".[dev]"
```

Run linting:
```bash
ruff check
ruff format
```

## License

MIT License