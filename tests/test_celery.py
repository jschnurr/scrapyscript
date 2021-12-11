import unittest

import scrapy
from celery import Celery
from scrapy.spiders import Spider
from scrapyscript import Job, Processor, ScrapyScriptException


class TitleSpider(Spider):
    name = "titlespider"

    def start_requests(self):
        yield scrapy.Request(self.url)

    def parse(self, response):
        page_title = response.xpath("//title/text()").extract_first()
        return {"data": page_title}


app = Celery("hello", broker="amqp://guest@localhost//")


@app.task
def celery_job(url):
    job = Job(TitleSpider, url=url)
    return Processor().run(job)


class ScrapyScriptCeleryTests(unittest.TestCase):
    def test_celery_job(self):
        # for unit testing, call celery synchronously
        task = celery_job.s("https://www.python.org").apply()
        self.assertGreater(len(task.result[0]["data"]), 0)
