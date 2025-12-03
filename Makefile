.PHONY: help install run clean

help:
	@echo "Available commands:"
	@echo "  install   Install dependencies (using uv)"
	@echo "  run       Run the application (using uv run)"
	@echo "  clean     Clean python cache files"

install:
	uv sync

run:
	uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + || true
	find . -type f -name "*.py[co]" -delete || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + || true