"""A tool for executing Python code in a sandboxed environment."""

import asyncio
import logging
from typing import Any

logger = logging.getLogger(__name__)


async def python_interpreter(code: str, timeout: int = 60) -> dict[str, Any]:
    """
    Executes a string of Python code and returns the output.

    Args:
        code: The Python code to execute.
        timeout: The timeout in seconds for the code execution.

    Returns:
        A dictionary containing the standard output, standard error, and return code.
    """
    logger.info(f"Executing Python code: {code}")
    # need to replace single quotes with double quotes for the shell command
    # Replace newlines with semicolons for single line execution
    code = code.replace("'", '"')
    try:
        process = await asyncio.create_subprocess_shell(
            f"python -c '{code}'",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=timeout)

        result = {
            "stdout": stdout.decode().strip(),
            "stderr": stderr.decode().strip(),
            "returncode": process.returncode,
        }
        logger.info(f"Execution result: {result}")
        return result

    except TimeoutError:
        logger.warning(f"Code execution timed out after {timeout} seconds.")
        return {
            "stdout": "",
            "stderr": f"TimeoutError: Code execution exceeded {timeout} seconds.",
            "returncode": -1,
        }
    except Exception as e:
        logger.error(f"An error occurred during code execution: {e}")
        return {"stdout": "", "stderr": str(e), "returncode": 1}
