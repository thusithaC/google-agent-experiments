"""Configuration management for agents_core."""

import logging.config
import sys

import structlog
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings


class MCPServerConfig(BaseSettings):
    """Configuration for MCP servers."""

    web_search_mcp_url: str = "http://localhost:8000/mcp"
    timeout: int = 10  # Timeout for MCP requests in seconds


class GeminiConfig(BaseSettings):
    """Configuration for Google Gemini."""

    gemini_api_key: str
    gemini_model: str = "gemini-2.5-flash"
    gemini_temperature: float = 0.1
    gemini_max_tokens: int = 8192


class AgentConfig(BaseModel):
    """Main configuration for the agent system."""

    # MCP server settings
    mcp: MCPServerConfig = Field(default_factory=MCPServerConfig)

    # Gemini settings
    gemini: GeminiConfig = Field(default_factory=GeminiConfig)

    # Logging
    log_level: str = "INFO"


def configure_logging(log_level: str = "INFO") -> None:
    """Configure structured logging with filename information."""

    # Configure standard logging
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=getattr(logging, log_level.upper()),
    )

    # Configure structlog processors
    processors = [
        # Add filename and line number to log records
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        structlog.processors.CallsiteParameterAdder(
            parameters=[
                structlog.processors.CallsiteParameter.FILENAME,
                structlog.processors.CallsiteParameter.LINENO,
                structlog.processors.CallsiteParameter.FUNC_NAME,
            ]
        ),
        structlog.processors.TimeStamper(fmt="ISO"),
        structlog.dev.ConsoleRenderer(),
    ]

    # Configure structlog
    structlog.configure(
        processors=processors,
        wrapper_class=structlog.stdlib.BoundLogger,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )


# Global configuration instance
config = AgentConfig()

# Configure logging on module import
configure_logging(config.log_level)
