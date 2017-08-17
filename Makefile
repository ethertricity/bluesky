ROOT := $(shell pwd)

clean:
	@echo "Cleaning source files..."
	@autopep8 -irav ${ROOT}
	@echo "Done!"


test:
	@python -m unittest tests
