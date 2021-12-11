.PHONY: lint test tox build clean

lint:
	poetry run black --check --diff src

test: lint
	poetry check
	poetry run pytest

tox:
	poetry run tox

build: clean test
	poetry build -vv

clean:
	rm -rf dist/
	rm -rf .pytest_cache/
	rm -rf src/scrapyscript.egg-info
	rm -rf .tox/
