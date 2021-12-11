import pytest
from scrapyscript import Job, Processor, ScrapyScriptException

from spiders import ParamReturnSpider, TitleSpider


def test_job_raises_if_no_spider_provided():
    with pytest.raises(TypeError):
        Job()


def test_create_valid_job():
    spider = TitleSpider
    job = Job(spider)
    assert isinstance(job, Job)
