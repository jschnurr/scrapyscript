<h1 align="center">
  <br>
  <a href="https://github.com/jschnurr/scrapyscript"><img src="https://i.ibb.co/ww3bNZ3/scrapyscript.png" alt="Scrapyscript"></a>
  <br>
</h1>

<h4 align="center">Embed Scrapy jobs directly in your code</h4>

<p align="center">
  <a href="https://github.com/jschnurr/scrapyscript/releases">
    <img src="https://img.shields.io/github/release/jschnurr/scrapyscript.svg">
  </a>

  <a href="https://pypi.org/project/scrapyscript/">
    <img src="https://img.shields.io/pypi/v/scrapyscript.svg">
  </a>

  <img src="https://github.com/jschnurr/scrapyscript/workflows/Tests/badge.svg">
  
  <img src="https://img.shields.io/pypi/pyversions/scrapyscript.svg">
</p>

### What is Scrapyscript?

Scrapyscript is a Python library you can use to run [Scrapy](https://github.com/scrapy/scrapy) spiders directly from your code. Scrapy is a great framework to use for scraping projects, but sometimes you don't need the whole framework, and just want to run a small spider from a script or a [Celery](https://github.com/celery/celery) job. That's where Scrapyscript comes in.

With Scrapyscript, you can:

- wrap regular Scrapy [Spiders](https://docs.scrapy.org/en/latest/topics/spiders.html) in a `Job`
- load the `Job(s)` in a `Processor`
- call `processor.run()` to execute them

... returning all results when the last job completes.

Let's see an example.

```python
import scrapy
from scrapyscript import Job, Processor

processor = Processor(settings=None)

class PythonSpider(scrapy.spiders.Spider):
    name = "myspider"

    def start_requests(self):
        yield scrapy.Request(self.url)

    def parse(self, response):
        data = response.xpath("//title/text()").extract_first()
        return {'title': data}

job = Job(PythonSpider, url="http://www.python.org")
results = processor.run(job)

print(results)
```

```json
[{ "title": "Welcome to Python.org" }]
```

See the [examples](examples/) directory for more, including a complete `Celery` example.

### Install

```python
pip install scrapyscript
```

### Requirements

- Linux or MacOS
- Python 3.8+
- Scrapy 2.5+

### API

#### Job (spider, \*args, \*\*kwargs)

A single request to call a spider, optionally passing in \*args or \*\*kwargs, which will be passed through to the spider constructor at runtime.

```python
# url will be available as self.url inside MySpider at runtime
myjob = Job(MySpider, url='http://www.github.com')
```

#### Processor (settings=None)

Create a multiprocessing reactor for running spiders. Optionally provide a `scrapy.settings.Settings` object to configure the Scrapy runtime.

```python
settings = scrapy.settings.Settings(values={'LOG_LEVEL': 'WARNING'})
processor = Processor(settings=settings)
```

#### Processor.run(jobs)

Start the Scrapy engine, and execute one or more jobs. Blocks and returns consolidated results in a single list.
`jobs` can be a single instance of `Job`, or a list.

```python
results = processor.run(myjob)
```

or

```python
results = processor.run([myjob1, myjob2, ...])
```

#### A word about Spider outputs

As per the [scrapy docs](https://doc.scrapy.org/en/latest/topics/spiders.html), a `Spider`
must return an iterable of `Request` and/or `dict` or `Item` objects.

Requests will be consumed by Scrapy inside the `Job`. `dict` or `scrapy.Item` objects will be queued
and output together when all spiders are finished.

Due to the way billiard handles communication between processes, each `dict` or `Item` must be
pickle-able using pickle protocol 0. **It's generally best to output `dict` objects from your Spider.**

### Contributing

Updates, additional features or bug fixes are always welcome.

#### Setup

- Install [Poetry](https://python-poetry.org/docs/#installation)
- `git clone git@github.com:jschnurr/scrapyscript.git`
- `poetry install`

#### Tests

- `make test` or `make tox`

### Version History

See [CHANGELOG.md](CHANGELOG.md)

### License

The MIT License (MIT). See LICENCE file for details.
