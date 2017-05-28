import unittest

from scrapy.settings import Settings
from scrapy.spiders import Spider
import scrapy

from scrapyscript import Job, Processor, ScrapyScriptException


class JobTests(unittest.TestCase):
    def test_create_valid_job(self):
        spider = Spider(name='testing')
        job = Job(spider)
        self.assertIsInstance(job.spider, Spider)

        job2 = Job(spider, {'data': 0})
        self.assertEqual(job2.payload['data'], 0)

    def test_not_a_spider_type(self):
        self.assertRaises(ScrapyScriptException, Job, 'not a spider')

    def test_no_spider_provided(self):
        self.assertRaises(TypeError, Job)

    def test_job_from_xpath(self):
        job = Job.from_xpath('http://www.python.org', '//title/text()')
        results = Processor().run(job)
        self.assertEqual(results[0]['data'][0],
                         'Welcome to Python.org')


class TestSpider(Spider):
    name = 'test'
    start_urls = ['http://www.python.org']

    def parse(self, response):
        ret = []
        ret.append({'bot': self.settings['BOT_NAME']})
        ret.append({'payload': self.payload})
        return ret


class ProcessorTests(unittest.TestCase):
    def test_settings_flow_through_to_spider(self):
        settings = Settings()
        settings['BOT_NAME'] = 'alpha'
        job = Job(TestSpider())
        results = Processor(settings=settings).run(job)

        self.assertIn({'bot': 'alpha'}, results)

    def test_payload_flows_through_to_spider(self):
        job = Job(TestSpider(), payload='apples')
        results = Processor().run(job)

        self.assertIn({'payload': 'apples'}, results)

    def test_mulitple_jobs(self):
        jobs = [
            Job.from_xpath('http://www.python.org', '//title/text()'),
            Job.from_xpath('http://www.python.org', '//title/text()'),
        ]

        results = Processor().run(jobs)
        self.assertEqual(len(results), 2)


class MyItem(scrapy.Item):
    name = scrapy.Field()

class TestItemSpider(Spider):
    name = 'testitemspider'
    start_urls = ['http://www.python.org']

    def parse(self, response):
        return MyItem(name='myitem')
