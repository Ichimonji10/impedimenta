.PHONY: help
help:
	@echo "Please use \`make <target>' where <target> is one of:"
	@echo "  help"
	@echo "    to show this message"
	@echo "  all"
	@echo "    to do all of the following"
	@echo "  lint"
	@echo "    to run all linters"
	@echo "  lint-mypy"
	@echo "    to run the mypy linter"
	@echo "  lint-pylint"
	@echo "    to run the pylint linter"
	@echo "  test"
	@echo "    to run all tests"
	@echo "  test-doctest"
	@echo "    to run doctest tests"
	@echo "  test-functional"
	@echo "    to run functional tests"
	@echo "  test-unit"
	@echo "    to run unit tests"

.PHONY: all
all: lint test

.PHONY: lint
lint: lint-mypy lint-pylint

.PHONY: lint-mypy
lint-mypy:
	mypy pp tests

.PHONY: lint-pylint
lint-pylint:
	pylint -j 0 pp tests

.PHONY: test
test: test-doctest test-unit test-functional

.PHONY:
test-doctest:
	python3 -m doctest pp/utils.py

.PHONY: test-unit
test-unit:
	python3 -m unittest discover --start-directory tests/unit --top-level-directory .

.PHONY: test-functional
test-functional:
	python3 -m unittest discover --start-directory tests/functional --top-level-directory .
