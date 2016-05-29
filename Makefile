.PHONY: clean test

help:
	@echo "test - run tests"
	@echo "clean - remove all build, test, coverage and Python artifacts"
	@echo "sdist - create an sdist"
	@echo "release - create an sdist and upload"

test: clean
	nosetests

sdist:
	python setup.py sdist

clean:
	find . -name '*.pyc' -delete

release:
	python setup.py sdist upload --sign
