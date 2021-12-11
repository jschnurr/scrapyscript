import unittest
import pytest

from scrapy.settings import Settings
from scrapy.spiders import Spider
import scrapy

from scrapyscript import Job, Processor, ScrapyScriptException


class MyItem(scrapy.Item):
    bot = scrapy.Field()
    data = scrapy.Field()


class MySpider(Spider):
    name = "myspider"

    def start_requests(self):
        yield scrapy.Request(self.url)

    def parse(self, response):
        title = response.xpath("//title/text()").extract_first()
        return MyItem(bot=self.settings["BOT_NAME"], data=title)


class BigSpider(Spider):
    name = "bigspider"

    def start_requests(self):
        yield scrapy.Request(self.url)

    def parse(self, response):
        longstr = "x" * 1073741824 * 2  # 2gb
        return longstr


class BadSpider(Spider):
    name = "badspider"

    def start_requests(self):
        yield scrapy.Request("http://www.python.org")

    def parse(self, response):
        return True


class ParamReturnSpider(Spider):
    name = "paramreturnspider"
    start_urls = ["http://www.python.org"]

    def __init__(self, category=None, *args, **kwargs):
        super(ParamReturnSpider, self).__init__(*args, **kwargs)
        self.category = category

    def parse(self, response):
        return dict(category=self.category, fruit=self.fruit)


class MyItemSpider(Spider):
    name = "myitemspider"

    def start_requests(self):
        yield scrapy.Request(self.url)

    def parse(self, response):
        title = response.xpath("//title/text()").extract_first()
        return MyItem(data=title + "x" * 1048576)


class ScrapyScriptTests(unittest.TestCase):
    def test_create_valid_job(self):
        spider = MySpider
        job = Job(spider)
        self.assertIsInstance(job, Job)

    def test_parameters_passed_to_spider(self):
        spider = ParamReturnSpider
        job = Job(spider, "cat1", fruit="banana")
        result = Processor().run(job)
        self.assertEqual(result, [dict(category="cat1", fruit="banana")])

    def test_no_spider_provided(self):
        self.assertRaises(TypeError, Job)

    def test_settings_flow_through_to_spider(self):
        settings = Settings()
        settings["BOT_NAME"] = "alpha"
        job = Job(MySpider, url="http://www.python.org")
        results = Processor(settings=settings).run(job)

        self.assertEqual(results[0]["bot"], "alpha")

    def test_multiple_jobs(self):
        jobs = [
            Job(MySpider, url="http://www.python.org"),
            Job(MySpider, url="http://www.github.com"),
        ]

        results = Processor().run(jobs)
        data = [item["data"].lower() for item in results]
        self.assertEqual(any("python" in s for s in data), True)
        self.assertEqual(any("github" in s for s in data), True)
        self.assertEqual(len(results), 2)

    def test_bad_return_value(self):
        job = Job(BadSpider, url="http://www.python.org")
        results = Processor().run(job)
        self.assertEqual(results, [])

    def test_big_return_value(self):
        job = Job(BigSpider, url="http://www.python.org")
        results = Processor().run(job)
        self.assertEqual(results, [])

    # larger, long running jobs can deadlock see https://github.com/jschnurr/scrapyscript/issues/3
    @pytest.mark.timeout(30)
    def test_for_deadlock(self):
        jobs = [Job(MyItemSpider, url="http://www.python.org") for i in range(50)]

        results = Processor().run(jobs)
        self.assertEqual(len(results), 50)


class ProcessorTests(unittest.TestCase):
    def test_item_scraped(self):
        p = Processor()
        p._item_scraped("test")
        self.assertEqual(p.items[0], "test")


if __name__ == "__main__":
    unittest.main()
