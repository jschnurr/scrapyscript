*Scrapy Script*

Minimalist interface for Scrapy, Python's favorite web scraping framework.

Scrapyscript (SS) allows you to invoke one or more spiders from a script, have them all run in parallel, and get the results back as a single list.  No scrapy project, no boilerplate, no hassle.

**Examples**
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

**API**
scrapyscript.Job = class Job(__builtin__.object)
 |  A job is a single request to call a specific spider, and optionally
 |  pass in a payload object which will be available inside the running spider.
 |  
 |  Methods defined here:
 |  
 |  __init__(self, spider, payload=None)
 |      Parms:
 |      spider (scrapy.spiders.Spider): the spider to be run for this job.
 |      payload - optional: Arbitrary object to be passed into the spider at
 |                          runtime.
 |  
 |  ----------------------------------------------------------------------
 |  Class methods defined here:
 |  
 |  from_xpath(cls, url, xpath, payload={}) from __builtin__.type
 |      Convenience method that returns a Job with a dynamically created
 |      spider.  The spider opens url, and returns the results of an xpath
 |      search of the response.
 |  

scrapyscript.Processor = class Processor(multiprocessing.process.Process)
 |  Start a twisted reactor and run the provided scrapy spiders.
 |  Blocks until all have finished.
 |  
 |  Methods defined here:
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
