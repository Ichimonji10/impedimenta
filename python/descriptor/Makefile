.PHONY: check
check: check-black check-mypy check-pylint check-pytest

.PHONY: check-black
check-black:
	poetry run black .

.PHONY: check-mypy
check-mypy:
	poetry run mypy .

.PHONY: check-pylint
check-pylint:
	poetry run pylint descriptor tests

.PHONY: check-pytest
check-pytest:
	poetry run pytest
