.PHONY: lint
lint:
	claude plugin validate .

.PHONY: plugin-update
plugin-update:
	@claude plugin marketplace add share-skills-local .claude-plugin/marketplace.json 2>&1 || claude plugin marketplace update share-skills-local 2>&1
	@if claude plugin list 2>&1 | grep -q "taipei-open-data-list"; then claude plugin update taipei-open-data-list@share-skills-local 2>&1; else claude plugin install taipei-open-data-list@share-skills-local 2>&1; fi
	@if claude plugin list 2>&1 | grep -q "data-visualizer"; then claude plugin update data-visualizer@share-skills-local 2>&1; else claude plugin install data-visualizer@share-skills-local 2>&1; fi