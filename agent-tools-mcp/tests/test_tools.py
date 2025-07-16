import pytest

from agent_tools_mcp.main import image_search, news_search, video_search, web_search


@pytest.mark.asyncio
async def test_web_search():
    """Tests the web_search tool."""
    query = "what is the capital of france"
    result = await web_search.fn(query)

    assert "error" not in result, f"Web search returned an error: {result.get('error')}"
    assert result["query"] == query
    assert "results" in result
    assert len(result["results"]) > 0


@pytest.mark.asyncio
async def test_image_search():
    """Tests the image_search tool."""
    query = "pictures of paris"
    result = await image_search.fn(query)

    assert "error" not in result, f"Image search returned an error: {result.get('error')}"
    assert result["query"] == query
    assert "results" in result
    assert len(result["results"]) > 0


@pytest.mark.asyncio
async def test_video_search():
    """Tests the video_search tool."""
    query = "tour of the eiffel tower"
    result = await video_search.fn(query)

    assert "error" not in result, f"Video search returned an error: {result.get('error')}"
    assert result["query"] == query
    assert "results" in result
    assert len(result["results"]) > 0


@pytest.mark.asyncio
async def test_news_search():
    """Tests the news_search tool."""
    query = "latest tech news"
    result = await news_search.fn(query)

    assert "error" not in result, f"News search returned an error: {result.get('error')}"
    assert result["query"] == query
    assert "results" in result
    assert len(result["results"]) > 0
