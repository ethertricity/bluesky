ROOT := $(shell pwd)

.PHONY: pep8
pep8:
	@echo "Cleaning source files..."
	@autopep8 -irav ${ROOT}
	@echo "Done!"

.PHONY: compile
compile:
	@python -m pep8 sparkl_cli
	@python -m pylint --ignore=test sparkl_cli

.PHONY: test
test:
	@python -m pytest

