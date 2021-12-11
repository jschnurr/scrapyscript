import scrapy


class MyItem(scrapy.Item):
    bot = scrapy.Field()
    data = scrapy.Field()
