'''
Run scrapy spiders from a script.

Blocks and runs all requests in parallel.  Accumulated items from all
spiders are returned as a list.
'''

import collections
from billiard import Process  # fork of multiprocessing that works with celery
from billiard.queues import Queue

from pydispatch import dispatcher
from scrapy import signals
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from scrapy.spiders import Spider


class ScrapyScriptException(Exception):
    pass


class Job(object):
    '''A job is a single request to call a specific spider, and optionally
    pass in a payload object which will be available inside the running spider.
    '''

    def __init__(self, spider, payload=None):
        '''Parms:
          spider (scrapy.spiders.Spider): the spider to be run for this job.
          payload - optional: Arbitrary object to be passed into the spider at
                              runtime.
        '''
        if not isinstance(spider, Spider):
            raise ScrapyScriptException(
                'Must provide instance of scrapy.spiders.Spider, got %s' %
                type(spider))

        self.spider = spider
        self.payload = payload

    @classmethod
    def from_xpath(cls, url, xpath, payload={}):
        '''Convenience method that returns a Job with a dynamically created
        spider.  The spider opens url, and returns the results of an xpath
        search of the response.'''

        def parse(self, response):
            return {'data': response.xpath(self._xpath).extract()}

        name = ''.join(ch for ch in url if ch.isalnum())
        spider = type('QuickSpider', (Spider, ), {
            'name': name,
            '_xpath': xpath,
            'start_urls': [url],
            'parse': parse,
        })

        return cls(spider(), payload=payload)


class Processor(Process):
    ''' Start a twisted reactor and run the provided scrapy spiders.
    Blocks until all have finished.
    '''

    def __init__(self, settings=None):
        '''
        Parms:
          settings (scrapy.settings.Settings) - settings to apply.  Defaults
        to Scrapy default settings.
        '''
        kwargs = {'ctx':__import__('billiard.synchronize')}

        self.results = Queue(**kwargs)
        self.items = []
        self.settings = settings or Settings()
        dispatcher.connect(self._item_passed, signals.item_passed)

    def _item_passed(self, item):
        self.items.append(item)

    def _crawl(self, requests):
        '''
        Parameters:
            requests (Request) - One or more Jobs. All will
                                 be loaded into a single invocation of the reactor.
        '''
        self.crawler = CrawlerProcess(self.settings)

        # crawl can be called multiple times to queue several requests
        for req in requests:
            self.crawler.crawl(req.spider, payload=req.payload)

        self.crawler.start()
        self.crawler.stop()
        self.results.put(self.items)

    def run(self, jobs):
        '''Start the Scrapy engine, and execute all jobs.  Return consolidated results
        in a single list.

        Parms:
          jobs ([Job]) - one or more Job objects to be processed.

        Returns:
          List of objects yielded by the spiders after all jobs have run.
        '''
        if not isinstance(jobs, collections.Iterable):
            jobs = [jobs]
        self.validate(jobs)

        p = Process(target=self._crawl, args=[jobs])
        p.start()
        p.join()
        p.terminate()

        return self.results.get()

    def validate(self, jobs):
        if not all([isinstance(x, Job) for x in jobs]):
            raise ScrapyScriptException('scrapyscript requires Job objects.')
