import scrapy
from scrapy.spiders import Spider

from items import MyItem


class TitleSpider(Spider):
    name = "titlespider"

    def start_requests(self):
        yield scrapy.Request(self.url)

    def parse(self, response):
        page_title = response.xpath("//title/text()").extract_first()
        return {"data": page_title}


class ItemSpider(Spider):
    name = "itemspider"

    def start_requests(self):
        yield scrapy.Request(self.url)

    def parse(self, response):
        title = response.xpath("//title/text()").extract_first()
        return MyItem(bot=self.settings["BOT_NAME"], data=title)


# returns positional argument as category, and fruit kwarg as fruit
class ParamReturnSpider(Spider):
    name = "paramreturnspider"
    start_urls = ["http://www.python.org"]

    def __init__(self, category=None, *args, **kwargs):
        super(ParamReturnSpider, self).__init__(*args, **kwargs)
        self.category = category

    def parse(self, response):
        return dict(category=self.category, fruit=self.fruit)


# returns an invalid object type
class BadSpider(Spider):
    name = "badspider"

    def start_requests(self):
        yield scrapy.Request("http://localhost")

    def parse(self, response):
        return True


# returns an item with a very large value
class BigSpider(Spider):
    name = "bigspider"

    def start_requests(self):
        yield scrapy.Request(self.url)

    def parse(self, response):
        longstr = "x" * 1024 * 250  # 250 mb
        return MyItem(data=longstr)
