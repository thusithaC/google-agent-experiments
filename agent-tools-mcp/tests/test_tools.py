import os

import pytest

from agent_tools_mcp.code_interpreter import python_interpreter
from agent_tools_mcp.search_tools import (
    image_search,
    news_search,
    video_search,
    web_search,
)


@pytest.mark.asyncio
async def test_web_search():
    """Tests the web_search tool."""
    query = "what is the capital of france"
    result = await web_search(query)

    assert "error" not in result, f"Web search returned an error: {result.get('error')}"
    assert result["query"] == query
    assert "results" in result
    assert len(result["results"]) > 0


@pytest.mark.asyncio
async def test_image_search():
    """Tests the image_search tool."""
    query = "pictures of paris"
    result = await image_search(query)

    assert "error" not in result, f"Image search returned an error: {result.get('error')}"
    assert result["query"] == query
    assert "results" in result
    assert len(result["results"]) > 0


@pytest.mark.asyncio
async def test_video_search():
    """Tests the video_search tool."""
    query = "tour of the eiffel tower"
    result = await video_search(query)

    assert "error" not in result, f"Video search returned an error: {result.get('error')}"
    assert result["query"] == query
    assert "results" in result
    assert len(result["results"]) > 0


@pytest.mark.asyncio
async def test_news_search():
    """Tests the news_search tool."""
    query = "latest tech news"
    result = await news_search(query)

    assert "error" not in result, f"News search returned an error: {result.get('error')}"
    assert result["query"] == query
    assert "results" in result
    assert len(result["results"]) > 0


@pytest.mark.asyncio
async def test_python_interpreter_success():
    """Tests the python_interpreter tool with valid code."""
    code = 'print("hello world")'  # noqa
    result = await python_interpreter(code)

    assert result["returncode"] == 0
    assert result["stdout"] == "hello world"
    assert result["stderr"] == ""


@pytest.mark.asyncio
async def test_python_interpreter_error():
    """Tests the python_interpreter tool with code that produces an error."""
    code = "print(1/0)"
    result = await python_interpreter(code)

    assert result["returncode"] == 1
    assert result["stdout"] == ""
    assert "ZeroDivisionError" in result["stderr"]


@pytest.mark.asyncio
async def test_python_interpreter_timeout():
    """Tests the python_interpreter tool with code that times out."""
    code = "import time; time.sleep(2)"
    result = await python_interpreter(code, timeout=1)

    assert result["returncode"] == -1
    assert "TimeoutError" in result["stderr"]


@pytest.mark.asyncio
async def test_python_interpreter_complex_script():
    """Tests the python_interpreter with a multi-line script from a file."""
    # Get the absolute path to the script
    script_path = os.path.join(os.path.dirname(__file__), "test_data", "complex_script.py")

    with open(script_path) as f:
        script_content = f.read()

    result = await python_interpreter(script_content)

    assert result["returncode"] == 0
    assert "The final result is: 55" in result["stdout"]
    assert "Script execution completed." in result["stdout"]
    assert result["stderr"] == ""
