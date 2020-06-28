.PHONY: lint test tox build

lint:
	poetry run black --check --diff --quiet src

test: lint
	poetry check
	poetry run pytest

tox:
	poetry run tox

build: pytest
	poetry build -vv
