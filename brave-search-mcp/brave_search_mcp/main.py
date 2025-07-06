"""Main module for Brave Search MCP Server."""

import json

from brave_search_python_client import (
    BraveSearch,
    CountryCode,
    ImagesSearchRequest,
    LanguageCode,
    NewsSearchRequest,
    VideosSearchRequest,
    WebSearchRequest,
)
from fastmcp import FastMCP

from .settings import settings

# Initialize the Brave Search client
bs = BraveSearch(api_key=settings.brave_search_api_key)

# Create the MCP server instance
server = FastMCP("brave-search-mcp")


@server.tool()
async def web_search(
    query: str,
    count: int = 10,
    country: str | None = None,
    search_lang: str | None = None,
    safe_search: str | None = None,
    freshness: str | None = None,
) -> str:
    """Search the web using Brave Search API.

    Args:
        query: The search query string
        count: Number of results to return (default: 10, max: 20)
        country: Country code for search results (e.g., 'US', 'DE', 'FR')
        search_lang: Language code for search results (e.g., 'en', 'de', 'fr')
        safe_search: Safe search filter ('strict', 'moderate', 'off')
        freshness: Freshness filter ('pd' for past day, 'pw' for past week, 'pm' for past month, 'py' for past year)

    Returns:
        Search results as a formatted JSON string
    """
    try:
        # Create the search request
        request = WebSearchRequest(
            q=query,
            count=min(count, 20),  # Limit to max 20 results
            country=CountryCode(country.upper()) if country else None,
            search_lang=LanguageCode(search_lang.lower()) if search_lang else None,
            safesearch=safe_search,
            freshness=freshness,
        )

        # Perform the search
        response = await bs.web(request)

        # Format the results
        results = []
        if response.web and response.web.results:
            for result in response.web.results:
                results.append(
                    {
                        "title": result.title,
                        "url": result.url,
                        "description": result.description,
                        "age": result.age,
                        "language": result.language,
                    }
                )

        return json.dumps(
            {"query": query, "total_results": len(results), "results": results}, indent=2
        )

    except Exception as e:
        return json.dumps({"error": f"Search failed: {str(e)}", "query": query}, indent=2)


@server.tool()
async def image_search(query: str, count: int = 10) -> str:
    """Search for images using Brave Search API.

    Args:
        query: The search query string
        count: Number of results to return (default: 10, max: 20)

    Returns:
        Image search results as a formatted JSON string
    """
    try:
        request = ImagesSearchRequest(q=query, count=min(count, 20))
        response = await bs.images(request)

        results = []
        if response.results:
            for image in response.results:
                results.append(
                    {
                        "title": image.title,
                        "url": image.url,
                        "thumbnail": image.thumbnail.src if image.thumbnail else None,
                        "source": image.source,
                        "properties": {
                            "width": image.properties.width if image.properties else None,
                            "height": image.properties.height if image.properties else None,
                            "format": image.properties.format if image.properties else None,
                        },
                    }
                )

        return json.dumps(
            {"query": query, "total_results": len(results), "results": results}, indent=2
        )

    except Exception as e:
        return json.dumps({"error": f"Image search failed: {str(e)}", "query": query}, indent=2)


@server.tool()
async def video_search(query: str, count: int = 10) -> str:
    """Search for videos using Brave Search API.

    Args:
        query: The search query string
        count: Number of results to return (default: 10, max: 20)

    Returns:
        Video search results as a formatted JSON string
    """
    try:
        request = VideosSearchRequest(q=query, count=min(count, 20))
        response = await bs.videos(request)

        results = []
        if response.results:
            for video in response.results:
                results.append(
                    {
                        "title": video.title,
                        "url": video.url,
                        "thumbnail": video.thumbnail.src if video.thumbnail else None,
                        "description": video.description,
                        "age": video.age,
                        "duration": video.duration,
                        "views": video.views,
                    }
                )

        return json.dumps(
            {"query": query, "total_results": len(results), "results": results}, indent=2
        )

    except Exception as e:
        return json.dumps({"error": f"Video search failed: {str(e)}", "query": query}, indent=2)


@server.tool()
async def news_search(query: str, count: int = 10) -> str:
    """Search for news articles using Brave Search API.

    Args:
        query: The search query string
        count: Number of results to return (default: 10, max: 20)

    Returns:
        News search results as a formatted JSON string
    """
    try:
        request = NewsSearchRequest(q=query, count=min(count, 20))
        response = await bs.news(request)

        results = []
        if response.results:
            for article in response.results:
                results.append(
                    {
                        "title": article.title,
                        "url": article.url,
                        "description": article.description,
                        "age": article.age,
                        "source": article.source,
                        "breaking": article.breaking,
                    }
                )

        return json.dumps(
            {"query": query, "total_results": len(results), "results": results}, indent=2
        )

    except Exception as e:
        return json.dumps({"error": f"News search failed: {str(e)}", "query": query}, indent=2)


if __name__ == "__main__":
    # Run the MCP server with HTTP transport
    # server.run(transport="http", host="0.0.0.0", port=8000, path="/mcp")
    server.run(transport="http", host=settings.server_host, port=settings.server_port, path="/mcp")
