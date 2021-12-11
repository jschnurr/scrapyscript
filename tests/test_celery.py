import scrapy
from celery import Celery
from scrapy.settings import Settings
from scrapy.spiders import Spider
from scrapyscript import Job, Processor, ScrapyScriptException


class TitleSpider(Spider):
    name = "titlespider"

    def start_requests(self):
        yield scrapy.Request(self.url)

    def parse(self, response):
        page_title = response.xpath("//title/text()").extract_first()
        return {"data": page_title}


class MyItem(scrapy.Item):
    bot = scrapy.Field()
    data = scrapy.Field()


class ItemSpider(Spider):
    name = "itemspider"

    def start_requests(self):
        yield scrapy.Request(self.url)

    def parse(self, response):
        title = response.xpath("//title/text()").extract_first()
        return MyItem(bot=self.settings["BOT_NAME"], data=title)


app = Celery("hello", broker="amqp://guest@localhost//")


@app.task
def celery_job(url):
    job = Job(TitleSpider, url=url)
    return Processor().run(job)


@app.task
def celery_job_with_custom_settings(url, settings):
    job = Job(ItemSpider, url=url)
    return Processor(settings=settings).run(job)


class TestScrapyScriptCelery:
    def test_celery_job(self):
        # for unit testing, call celery synchronously
        task = celery_job.s("https://www.python.org").apply()
        assert len(task.result[0]["data"]) > 0

    def test_celery_job_with_settings(self):
        settings = Settings()
        settings["BOT_NAME"] = "alpha"

        task = celery_job_with_custom_settings.s(
            "https://www.python.org", settings
        ).apply()
        print(task.result[0])
        assert task.result[0]["bot"] == "alpha"
