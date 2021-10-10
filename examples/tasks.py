import scrapy
from celery import Celery
from scrapy.spiders import Spider
from scrapyscript import Job, Processor


class MySpider(Spider):
    name = "myspider"

    def start_requests(self):
        yield scrapy.Request(self.url)

    def parse(self, response):
        page_title = response.xpath("//title/text()").extract_first()
        return {"data": page_title}


# Depends on localhost running rabbitmq-server and `poetry run celery -A tasks worker`
app = Celery("tasks", backend="rpc://", broker="pyamqp://guest@localhost//")


@app.task
def celery_job(url):
    job = Job(MySpider, url=url)
    return Processor().run(job)


if __name__ == "__main__":
    task = celery_job.s("https://www.python.org").delay()
    result = task.get()
    print(result)
