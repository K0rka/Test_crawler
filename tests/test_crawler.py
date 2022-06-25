import pytest
from unittest.mock import ANY, call
from requests import Response

from src.utils.crawler import Crawler


@pytest.fixture
def mock_response_200():
    fake_response = Response()
    fake_response.status_code = 200
    fake_response._content = b'{"status": "ok"}'
    return fake_response

@pytest.fixture
def mock_response_400():
    fake_response = Response()
    fake_response.status_code = 400
    fake_response._content = b'{"status": "error", "errors": ["400 error"]}'
    return fake_response

def dummy_url_validator(url):
    return url


def test_crowl_with_some_links(mocker):
    # given
    logger = mocker.Mock()
    test_crawler = Crawler("https://test_url", logger)

    mocked_crawler_results = mocker.patch.object(test_crawler, "crawler_results")
    mocked_results_from_url = mocker.patch.object(test_crawler, "_get_results_for_url")
    mocked_validator = mocker.patch.object(Crawler, "_validate_url")
    mocked_validator.side_effect = dummy_url_validator

    mocked_results_from_url.side_effect = [
        ["/found_url_1/path=23", "/found_url_2/id=2", "https://url.three"],
        [],
        [],
    ]

    # when
    test_crawler.crawl()

    # then
    mocked_crawler_results.add_results.assert_has_calls(
        [
            call('https://test_url', ['/found_url_1/path=23', '/found_url_2/id=2', 'https://url.three']),
            call("https://test_url/found_url_1/path=23", []),
            call("https://test_url/found_url_2/id=2", []),
        ],
        any_order=True
    )
    mocked_validator.assert_has_calls([call("https://test_url"),
                                       call("https://test_url/found_url_1/path=23"),
                                       call("https://test_url/found_url_2/id=2")],
                                      any_order=True)


def test_crawler_invalid_starting_url(mocker):
    pass

def test_validate_url(mocker):
    pass

def test_add_new_links_to_visit(mocker):
    pass

def test_get_reuslts_for_url(mocker, mock_response_200):
    # given
    logger = mocker.Mock()
    test_crawler = Crawler("https://test_url", logger)
    mocked_bs_find_all = mocker.patch("src.utils.crawler.BeautifulSoup.find_all")
    mocked_requests = mocker.patch("src.utils.crawler.requests.get", return_value=mock_response_200)

    # when
    test_crawler._get_results_for_url("https://test_url")

    # then
    mocked_requests.assert_called_once_with("https://test_url", ANY)
    mocked_bs_find_all.assert_has_calls([call("a")])

def test_error_get_reuslts_for_url(mocker, mock_response_400):
    # given
    logger = mocker.Mock()
    test_crawler = Crawler("https://test_url", logger)
    mocked_bs_find_all = mocker.patch("src.utils.crawler.BeautifulSoup.find_all")
    mocked_requests = mocker.patch("src.utils.crawler.requests.get", return_value=mock_response_200)

    # when
    test_crawler._get_results_for_url("https://test_url")

    # then
    mocked_requests.assert_called_once_with("https://test_url", ANY)
    mocked_bs_find_all.assert_not_called()