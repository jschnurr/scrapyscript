*Overview*

Scrapyscript provides a minimalist interface for invoking Scrapy directly
from your code. Define Jobs that include your spider and any object
you would like to pass to the running spider, and then pass them to an
instance of Processor which will block, run the spiders, and return a list
of consolidated results.

Useful for leveraging the vast power of Scrapy from existing code, or to
run Scrapy from a Celery job.

*Requirements*
- Python 2.7 or 3.4
- Tested on Linux only (other platforms may work as well)

*Install*
```python
pip install scrapyscript
```

*Examples*
Let's create a spider that retrieves the title attribute from www.python.org.

``` python
from scrapyscript import Job, Processor
from scrapy.spiders import Spider

class PythonSpider(Spider):
    name = 'myspider'
    start_urls = ['http://www.python.org']

    def parse(self, response):
        title = response.xpath('//title/text()').extract()
        return {'title': title}

job = Job(PythonSpider())
Processor().run(job)
```

``` text
[{'title': [u'Welcome to Python.org']}]
```

There is also a convenience function that supports one xpath query against one URL:

``` python
job = Job.from_xpath('http://www.python.org', '//title/text()')
Processor().run(job)
```

``` text
[{'data': [<Selector xpath='//title/text()' data=u'Welcome to Python.org'>]}]
```

*Jobs*
 A job is a single request to call a specific spider, and optionally
 pass in a payload object which will be available inside the running spider.

``` text
scrapyscript.Job = class Job(object)
 |  
 |  __init__(self, spider, payload=None)
 |      Parms:
 |      spider (scrapy.spiders.Spider): the spider to be run for this job.
 |      payload - optional: Arbitrary object to be passed into the spider at
 |                          runtime.
 |  
 |  ----------------------------------------------------------------------
 |  Class methods:
 |  
 |  from_xpath(cls, url, xpath, payload={})
 |      Convenience method that returns a Job with a dynamically created
 |      spider.  The spider opens url, and returns the results of an xpath
 |      search of the response.
 |  
```

*Processor*
 Start a twisted reactor and run the provided scrapy spiders.
 Blocks until all have finished.
```text
scrapyscript.Processor = class Processor(billiard.process.Process)
 |  
 |  Methods:
 |  
 |  __init__(self, settings=None)
 |      Parms:
 |        settings (scrapy.settings.Settings) - settings to apply.  Defaults
 |      to Scrapy default settings.
 |  
 |  run(self, jobs)
 |      Start the Scrapy engine, and execute all jobs.  Return consolidated results
 |      in a single list.
 |      
 |      Parms:
 |        jobs ([Job]) - one or more Job objects to be processed.
 |      
 |      Returns:
 |        List of objects yielded by the spiders after all jobs have run.
 |  
```

*Notes*
**Multiprocessing vs Billiard**
Scrapyscript spawns a subprocess to support the Twisted reactor. Billiard
provides a fork of the multiprocessing library that supports Celery. This
allows you to schedule scrapy spiders to run as Celery tasks.

*Tests*
Run all tests:
```bash
tox
```

*Contributing*
Updates, additional features or bug fixes are always welcome.

*License*
The MIT License (MIT). See LICENCE file for details.
