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
	@echo "Running ruff check --fix and ruff format on brave-search-mcp..."
	cd brave-search-mcp && uv run ruff check --fix --unsafe-fixes .
	cd brave-search-mcp && uv run ruff format .
	@echo "Formatting complete!"

# Lint target - runs ruff check without fixing (for CI/validation)
lint:
	@echo "Running ruff check on agents-core..."
	cd agents-core && uv run ruff check .
	cd agents-core && uv run ruff format --check .
	@echo "Running ruff check on brave-search-mcp..."
	cd brave-search-mcp && uv run ruff check .
	cd brave-search-mcp && uv run ruff format --check .
	@echo "Linting complete!"
