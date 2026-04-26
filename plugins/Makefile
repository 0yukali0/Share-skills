PHONY: lint
lint:
	claude plugin validate .

.PHONY: plugin-update
plugin-update:
	@claude plugin marketplace update share-skills-local 2>&1
	@claude plugin update taipei-open-data-list@share-skills-local
 2>&1