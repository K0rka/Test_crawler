import pytest
from unittest.mock import call

from src import crawl
from src.crawl import handler


@pytest.fixture(autouse=True)
def mock_logger(mocker):
    logger = mocker.patch.object(crawl, "logger")

    return logger

def test_handler(mocker, mock_logger):
    mock_url = "https://example_url"
    crawl_mock = mocker.patch(
        "src.crawl.Crawler.crawl",
    )
    handler(mock_url)

    crawl_mock.assert_called_once()
    mock_logger.log_info.has_calls(
        [call(f"Start crawling with {mock_url}"), call(f"Finished crawling for {mock_url}")]
    )
    mock_logger.log_metric.assert_called_once_with("process_succeeded", 1)



def test_handler_throw(mocker, mock_logger):
    mock_url = "https://another_example_url"
    crawl_mock = mocker.patch(
        "src.crawl.Crawler.crawl",
    )
    crawl_mock.side_effect = ValueError("Some value is wrong")
    handler(mock_url)
    crawl_mock.assert_called_once()
    mock_logger.log_info.has_calls(
        [call(f"Start crawling with {mock_url}"), call(f"Finished crawling for {mock_url}")]
    )
    mock_logger.log_error.assert_called_once_with(f"Failed with some value is wrong")
    mock_logger.log_metric.assert_called_once_with("process_failed", 1)
