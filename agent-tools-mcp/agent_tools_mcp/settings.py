"""Settings configuration for Brave Search MCP Server."""

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    brave_search_api_key: str = Field(
        ..., description="Brave Search API key", env="BRAVE_SEARCH_API_KEY"
    )

    server_host: str = Field(
        default="0.0.0.0", description="Server host address", env="SERVER_HOST"
    )

    server_port: int = Field(default=8000, description="Server port number", env="SERVER_PORT")

    log_level: str = Field(default="info", description="Log level for the server", env="LOG_LEVEL")


# Create a global settings instance
settings = Settings()
