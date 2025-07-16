FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Install uv package manager
RUN pip install uv

# Copy pyproject.toml and uv.lock first (for better Docker layer caching)
COPY pyproject.toml uv.lock README.md ./

# Install dependencies using uv (without installing the root project)
RUN uv sync --no-install-project

# Copy the source code
COPY agent_tools_mcp/ ./agent_tools_mcp/
COPY scripts/run_server.sh ./scripts/

RUN uv sync

# Expose port 8000
EXPOSE 8000

# Set environment variables
ENV PYTHONPATH=/app \
    PYTHONUNBUFFERED=1 \
    PATH="/app/.venv/bin:${PATH}"

# Run the server using the start script
CMD ["./scripts/run_server.sh"]
