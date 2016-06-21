.PHONY: clean test sdist release

help:
	@echo "test - run tox tests"
	@echo "clean - remove all build, test, coverage and Python artifacts"
	@echo "sdist - create an sdist"
	@echo "release - create an sdist and upload to pypi"
	@echo "test-release - create an sdist and upload to testpypi"

test: clean
	tox

sdist:
	python setup.py sdist

clean:
	find . -name '*.pyc' -delete

release:
	python setup.py sdist upload -r pypi

test-release:
	python setup.py sdist upload -r pypitest
