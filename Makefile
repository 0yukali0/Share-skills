.PHONY: fmt
fmt:
	@echo "Formatting code..."
	@isort .
	@ruff format .
	@ruff check --fix .