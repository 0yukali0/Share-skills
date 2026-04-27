.PHONY: lint
lint:
	make -C plugins lint

.PHONY: plugin-update
plugin-update:
	make -C plugins plugin-update

.PHONY: fmt
fmt:
	@echo "Formatting code..."
	@isort .
	@ruff format .
	@ruff check --fix 