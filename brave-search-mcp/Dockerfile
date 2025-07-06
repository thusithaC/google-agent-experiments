# Use Python 3.12 slim image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install uv package manager
RUN pip install uv

# Copy pyproject.toml and uv.lock first (for better Docker layer caching)
COPY pyproject.toml uv.lock README.md ./

# Install dependencies using uv (without installing the root project)
RUN uv sync --no-install-project

# Copy the source code
COPY brave_search_mcp/ ./brave_search_mcp/
COPY run_server.sh ./

RUN uv sync

# Make the run script executable
RUN chmod +x run_server.sh

# Expose port 8000
EXPOSE 8000

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Run the server using the start script
CMD ["./run_server.sh"]
