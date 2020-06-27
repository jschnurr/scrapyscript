import unittest

from scrapy.settings import Settings
from scrapy.spiders import Spider
import scrapy

from scrapyscript import Job, Processor, ScrapyScriptException


class MySpider(Spider):
    name = 'myspider'

    def start_requests(self):
        yield scrapy.Request(self.url)

    def parse(self, response):
        title = response.xpath('//title/text()').extract()
        ret = []
        ret.append({'bot': self.settings['BOT_NAME']})
        ret.append({'title': title})
        return ret


class BadSpider(Spider):
    name = 'badspider'

    def start_requests(self):
        yield scrapy.Request('http://www.python.org')

    def parse(self, response):
        return {'payload': response}  # cannot be pickled with proto 0


class ParamReturnSpider(Spider):
    name = 'myspider'
    start_urls = ['http://www.python.org']

    def __init__(self, category=None, *args, **kwargs):
        super(ParamReturnSpider, self).__init__(*args, **kwargs)
        self.category = category

    def parse(self, response):
        return dict(category=self.category, fruit=self.fruit)


class ScrapyScriptTests(unittest.TestCase):
    def test_create_valid_job(self):
        spider = MySpider
        job = Job(spider)
        self.assertIsInstance(job, Job)

    def test_parameters_passed_to_spider(self):
        spider = ParamReturnSpider
        job = Job(spider, 'cat1', fruit='banana')
        result = Processor().run(job)
        self.assertEqual(result, [dict(category='cat1', fruit='banana')])

    def test_no_spider_provided(self):
        self.assertRaises(TypeError, Job)

    def test_settings_flow_through_to_spider(self):
        settings = Settings()
        settings['BOT_NAME'] = 'alpha'
        job = Job(MySpider, url='http://www.python.org')
        results = Processor(settings=settings).run(job)

        self.assertIn({'bot': 'alpha'}, results)

    def test_mulitple_jobs(self):
        jobs = [
            Job(MySpider, url='http://www.python.org'),
            Job(MySpider, url='http://www.github.com')
        ]

        results = Processor().run(jobs)
        self.assertEqual(len(results), 4)

    # def test_bad_return_value(self):
    #     job = Job(TestBadSpider, url='http://www.python.org')
    #     results = Processor().run(job)
    #     self.assertEqual(len(results), 4)

if __name__ == '__main__':
    unittest.main()