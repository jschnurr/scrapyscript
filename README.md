![Build](https://github.com/jschnurr/scrapyscript/workflows/Tests/badge.svg) [![PyPI](https://img.shields.io/pypi/v/scrapyscript.svg)](https://pypi.org/project/scrapyscript/)

# Overview

Scrapyscript provides a minimalist interface for invoking Scrapy directly
from your code. Define Jobs that include your spider and any object
you would like to pass to the running spider, and then pass them to an
instance of Processor which will block, run the spiders, and return a list
of consolidated results.

Useful for leveraging the vast power of Scrapy from existing code, or to
run Scrapy from a Celery job.

# Requirements

- Python 3.6+
- Tested on Linux only (other platforms may work as well)

# Install

```python
pip install scrapyscript
```

# Example

Let's create a spider that retrieves the title attribute from two popular websites.

``` python
from scrapyscript import Job, Processor
from scrapy.spiders import Spider
from scrapy import Request
import json

# Define a Scrapy Spider, which can accept *args or **kwargs
# https://doc.scrapy.org/en/latest/topics/spiders.html#spider-arguments
class PythonSpider(Spider):
    name = 'myspider'

    def start_requests(self):
        yield Request(self.url)

    def parse(self, response):
        title = response.xpath('//title/text()').extract()
        return {'url': response.request.url, 'title': title}

# Create jobs for each instance. *args and **kwargs supplied here will
# be passed to the spider constructor at runtime
githubJob = Job(PythonSpider, url='http://www.github.com')
pythonJob = Job(PythonSpider, url='http://www.python.org')

# Create a Processor, optionally passing in a Scrapy Settings object.
processor = Processor(settings=None)

# Start the reactor, and block until all spiders complete.
data = processor.run([githubJob, pythonJob])

# Print the consolidated results
print(json.dumps(data, indent=4))
```

``` json
[
    {
        "title": [
            "Welcome to Python.org"
        ],
        "url": "https://www.python.org/"
    },
    {
        "title": [
            "The world's leading software development platform \u00b7 GitHub",
            "1clr-code-hosting"
        ],
        "url": "https://github.com/"
    }
]
```

# Spider Output Types
As per the [scrapy docs](https://doc.scrapy.org/en/latest/topics/spiders.html), a Spider
must return an iterable of **Request** and/or **dicts** or **Item** objects.

Requests will be consumed by Scrapy inside the Job. Dicts or Item objects will be queued
and output together when all spiders are finished.

Due to the way billiard handles communication between processes, each dict or item must be
pickle-able using pickle protocol 0.

# Jobs
 A job is a single request to call a specific spider, optionally passing in
 *args or **kwargs, which will be passed through to the spider constructor at runtime.

```python
def __init__(self, spider, *args, **kwargs):
    '''Parameters:
        spider (spidercls): the spider to be run for this job.
    '''
```

# Processor
A Twisted reactor for running spiders. Blocks until all have finished.

## Constructor

```python
class Processor(Process):
    def __init__(self, settings=None):
        '''
        Parameters:
          settings (scrapy.settings.Settings) - settings to apply. Defaults to Scrapy defaults.
        '''
```

## Run

Starts the Scrapy engine, and executes all jobs.  Returns consolidated results in a single list.

```python
    def run(self, jobs):
        '''
        Parameters:
            jobs ([Job]) - one or more Job objects to be processed.

        Returns:
            List of objects yielded by the spiders after all jobs have run.
        '''
```

# Notes

## Multiprocessing vs Billiard

Scrapyscript spawns a subprocess to support the Twisted reactor. Billiard
provides a fork of the multiprocessing library that supports Celery. This
allows you to schedule scrapy spiders to run as Celery tasks.

# Contributing

Updates, additional features or bug fixes are always welcome.

## Setup
- Install (Poetry)[https://python-poetry.org/docs/#installation]
- `poetry install`

## Tests
- `make test` or `make tox`

# Version History

- 1.1.0 - 27-Jun-2020 - Python 3.6+ only, dependency version bumps
- 1.0.0 - 10-Dec-2017 - API changes to pass *args and **kwargs to running spider
- 0.1.0 - 28-May-2017 - patches to support Celery 4+ and Billiard 3.5.+. Thanks to @mrge and @bmartel.

# License

The MIT License (MIT). See LICENCE file for details.
