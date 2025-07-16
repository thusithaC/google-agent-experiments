"""Main module for Brave Search MCP Server."""

from typing import Any

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

from agent_tools_mcp.settings import settings

# Initialize the Brave Search client
bs = BraveSearch(api_key=settings.brave_search_api_key)

# Create the MCP server instance
server = FastMCP("agent-tools-mcp")


@server.tool()
async def web_search(
    query: str,
    count: int = 10,
    country: str | None = None,
    search_lang: str | None = None,
    safe_search: str | None = None,
    freshness: str | None = None,
) -> dict[str, Any]:
    """Search the web using Brave Search API.

    Args:
        query: The search query string
        count: Number of results to return (default: 10, max: 20)
        country: Country code for search results (e.g., 'US', 'DE', 'FR')
        search_lang: Language code for search results (e.g., 'en', 'de', 'fr')
        safe_search: Safe search filter ('strict', 'moderate', 'off')
        freshness: Freshness filter ('pd' for past day, 'pw' for past week, 'pm' for past month, 'py' for past year)

    Returns:
        Search results as a dictionary.
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
                        "url": str(result.url),
                        "description": result.description,
                        "age": result.age,
                        "language": result.language,
                    }
                )

        return {"query": query, "total_results": len(results), "results": results}

    except Exception as e:
        return {"error": f"Search failed: {str(e)}", "query": query}


@server.tool()
async def image_search(query: str, count: int = 10) -> dict[str, Any]:
    """Search for images using Brave Search API.

    Args:
        query: The search query string
        count: Number of results to return (default: 10, max: 20)

    Returns:
        Image search results as a dictionary.
    """
    try:
        request = ImagesSearchRequest(q=query, count=min(count, 20))
        response = await bs.images(request)

        results = []
        if response.results:
            for image in response.results:
                properties_data = None
                if image.properties:
                    properties_data = {
                        "url": str(image.properties.url)
                        if hasattr(image.properties, "url")
                        else None,
                        "placeholder": str(image.properties.placeholder)
                        if hasattr(image.properties, "placeholder")
                        else None,
                    }

                results.append(
                    {
                        "title": image.title,
                        "url": str(image.url),
                        "thumbnail": str(image.thumbnail.src) if image.thumbnail else None,
                        "source": image.source,
                        "properties": properties_data,
                    }
                )

        return {"query": query, "total_results": len(results), "results": results}

    except Exception as e:
        return {"error": f"Image search failed: {str(e)}", "query": query}


@server.tool()
async def video_search(query: str, count: int = 10) -> dict[str, Any]:
    """Search for videos using Brave Search API.

    Args:
        query: The search query string
        count: Number of results to return (default: 10, max: 20)

    Returns:
        Video search results as a dictionary.
    """
    try:
        request = VideosSearchRequest(q=query, count=min(count, 20))
        response = await bs.videos(request)

        results = []
        if response.results:
            for video in response.results:
                video_data = {
                    "title": video.title,
                    "url": str(video.url),
                    "thumbnail": str(video.thumbnail.src) if video.thumbnail else None,
                    "description": video.description,
                    "age": video.age,
                }
                if video.video:
                    video_data.update(
                        {
                            "duration": video.video.duration,
                            "views": video.video.views,
                            "creator": video.video.creator,
                            "publisher": video.video.publisher,
                        }
                    )
                results.append(video_data)

        return {"query": query, "total_results": len(results), "results": results}

    except Exception as e:
        return {"error": f"Video search failed: {str(e)}", "query": query}


@server.tool()
async def news_search(query: str, count: int = 10) -> dict[str, Any]:
    """Search for news articles using Brave Search API.

    Args:
        query: The search query string
        count: Number of results to return (default: 10, max: 20)

    Returns:
        News search results as a dictionary.
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
                        "url": str(article.url),
                        "description": article.description,
                        "age": article.age,
                        "breaking": article.breaking,
                    }
                )

        return {"query": query, "total_results": len(results), "results": results}

    except Exception as e:
        return {"error": f"News search failed: {str(e)}", "query": query}


if __name__ == "__main__":
    # For development, run the server directly
    server.run(transport="http", host=settings.server_host, port=settings.server_port, path="/mcp")
