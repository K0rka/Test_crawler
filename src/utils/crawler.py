from bs4 import BeautifulSoup
import requests
from src.utils.crawler_results import CrowlerResult

# 1. Validate url: it shouldn't start with https, we can try to assume it. If there's no https working, let customer know and config to
# 2. Delete / in the end of the root url, otherwise it might be double / when we add relative path

# Class which is responsible for iterating through all the required urls
class Crawler:
    headers = requests.utils.default_headers()

    #  There's no order requirements, so iterating over set is ok. QQ: how it will react for set being updated
    urls_to_visit = set()

    def __init__(self, url, logger):
        self.crawler_results = CrowlerResult(logger)
        self.urls_to_visit.add(url)
        self.logger = logger

    def crawl(self):
        next_one = self.crawler_results.next_url_to_check()
        while next_one != None:
            results = self._get_results_for_url(next_one)
            self.crawler_results.add_results(next_one, results)
            self._add_new_links_to_visit(results)
            next_one = self._next_url_to_check()

    def _get_results_for_url(self, url):
        try:
            req = requests.get(url, self.headers)
            soup = BeautifulSoup(req.content, "html.parser")
            local_links = set()
            for link in soup.find_all("a"):
                local_links.add(link.get("href"))
            return local_links
        except Exception as e:
            self.logger.log_error(f"crawling {url} failed with {e}")

    def _validate_url(self, url):
        # Take care of http start case
        if not url.startswith("https://"):
            url = "https://" + url
        if requests.head(url).status_code == 200:
            return url
        return None

    def _next_url_to_check(self):
        url = self.urls_to_visit.pop()
        return self.__validate_url(url)

    def _add_new_links_to_visit(self, found_links):
        root_url = self.initial_url
        for next_link in found_links:
            if next_link is None or len(next_link) == 0:
                print(f"WTF: {next_link}")
            # assuming this is relative link
            if next_link.startswith("/"):
                next_link = root_url + next_link
            if next_link.startswith(root_url) and self.results.get(next_link) is None:
                self.urls_to_visit.add(next_link)
