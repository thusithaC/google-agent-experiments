.PHONY: format lint help

# Default target
help:
	@echo "Available targets:"
	@echo "  format  - Run ruff check --fix and ruff format on all subprojects"
	@echo "  lint    - Run ruff check without fixing (for CI/validation)"
	@echo "  help    - Show this help message"

# Format target - runs ruff check --fix and ruff format on both subprojects
format:
	@echo "Running ruff check --fix and ruff format on agents-core..."
	cd agents-core && uv run ruff check --fix --unsafe-fixes .
	cd agents-core && uv run ruff format .
	@echo "Running ruff check --fix and ruff format on agent-tools-mcp..."
	cd agent-tools-mcp && uv run ruff check --fix --unsafe-fixes .
	cd agent-tools-mcp && uv run ruff format .
	@echo "Formatting complete!"

# Lint target - runs ruff check without fixing (for CI/validation)
lint:
	@echo "Running ruff check on agents-core..."
	cd agents-core && uv run ruff check .
	cd agents-core && uv run ruff format --check .
	@echo "Running ruff check on agent-tools-mcp..."
	cd agent-tools-mcp && uv run ruff check .
	cd agent-tools-mcp && uv run ruff format --check .
	@echo "Linting complete!"


# Build - build docker images for both subprojects.
build:
	@echo "Building docker images for agents-core and agent-tools-mcp..."
	docker-compose build
	@echo "Build complete!"

# Clean - kill docker containers through docker-compose and cleanup.
clean:
	@echo "Cleaning up docker containers..."
	docker-compose down --remove-orphans
	@echo "Cleanup complete!"