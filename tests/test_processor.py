import pytest
from scrapy.settings import Settings
from scrapyscript import Job, Processor, ScrapyScriptException

from spiders import BadSpider, BigSpider, ItemSpider, ParamReturnSpider, TitleSpider


def test_item_scraped_appends_items():
    p = Processor()
    p._item_scraped("test")
    assert p.items[0] == "test"


def test_job_validate_raises_exception_if_not_jobs():
    with pytest.raises(ScrapyScriptException):
        jobs = [Job(TitleSpider, url="http://www.python.org"), "not a Job"]
        p = Processor()
        p.validate(jobs)


def test_run_calls_process_join_terminate(mocker):
    mock_proc = mocker.patch("scrapyscript.Process")
    mock_q = mocker.patch("scrapyscript.Queue")

    job = Job(TitleSpider, url="http://www.python.org")
    print(Processor().run(job))
    mock_proc().start.assert_called_once()
    mock_proc().join.assert_called_once()
    mock_proc().terminate.assert_called_once()


def test_args_kwargs_passed_to_spider():
    spider = ParamReturnSpider
    job = Job(spider, "cat1", fruit="banana")
    result = Processor().run(job)
    assert result == [dict(category="cat1", fruit="banana")]


def test_settings_flow_through_to_spider():
    settings = Settings()
    settings["BOT_NAME"] = "alpha"
    job = Job(ItemSpider, url="http://www.python.org")
    results = Processor(settings=settings).run(job)

    assert results[0]["bot"] == "alpha"


def test_multiple_jobs_return_job_specific_data_in_each_result():
    jobs = [
        Job(TitleSpider, url="http://www.python.org"),
        Job(TitleSpider, url="http://www.github.com"),
    ]

    results = Processor().run(jobs)
    data = [item["data"].lower() for item in results]
    assert any("python" in s for s in data)
    assert any("github" in s for s in data)
    assert len(results) == 2


def test_bad_return_value():
    job = Job(BadSpider)
    results = Processor().run(job)
    assert results == []


def test_big_return_value():
    job = Job(BigSpider, url="http://www.python.org")
    results = Processor().run(job)
    assert len(results) == 1


# larger, long running jobs can deadlock see https://github.com/jschnurr/scrapyscript/issues/3
@pytest.mark.timeout(30)
def test_for_deadlock():
    jobs = [Job(TitleSpider, url="http://www.python.org") for i in range(50)]

    results = Processor().run(jobs)
    assert len(results) == 50


def test_crawl_calls_crawlerprocess_with_correct_params(mocker):
    mock_crawl = mocker.patch("scrapyscript.CrawlerProcess")
    mock_crawl().crawl.return_value = None
    mock_crawl().start.return_value = None
    mock_crawl().stop.return_value = None

    url = "http://www.python.org"
    job = Job(TitleSpider, url=url)
    Processor()._crawl([job])

    mock_crawl().crawl.assert_called_with(job.spider, url=url)
    mock_crawl().start.assert_called_once()
    mock_crawl().stop.assert_called_once()
