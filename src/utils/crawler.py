from bs4 import BeautifulSoup
import requests
from src.utils.crawler_results import CrowlerResult

# 2. Delete / in the end of the root url, otherwise it might be double / when we add relative path

# Class which is responsible for iterating through all the required urls
# Assumptions:
# - Link is everything in "a href" tags
# - There's no any required order for going to links or saving them
class Crawler:
    headers = requests.utils.default_headers()

    #  There's no order requirements, so iterating over set is ok. QQ: how it will react for set being updated
    urls_to_visit = set()
    visited_urls = set()

    def __init__(self, url, logger):
        self.crawler_results = CrowlerResult(logger)
        self.initial_url = url
        self.urls_to_visit = set()
        self.visited_urls = set()

        self.urls_to_visit.add(url)
        self.logger = logger

    def crawl(self):
        next_one = self._next_url_to_check()
        # Going through all the links that have and
        # 1. Mark link as visited
        # 2. Update results (=print them)
        # 3. Add new links to the list for visit
        # 4. Get next link
        while next_one is not None:
            results = self._get_results_for_url(next_one)
            self.visited_urls.add(next_one)
            self.crawler_results.add_results(next_one, results)
            self._add_new_links_to_visit(results)
            next_one = self._next_url_to_check()

    def _get_results_for_url(self, url):
        try:
            req = requests.get(url, self.headers)
            if req.status_code != 200:
                self.logger.log_error(f"Error getting data from url: {url}, error: {req.status_code}")
                return
            soup = BeautifulSoup(req.content, "html.parser")
            local_links = set()
            # Extracting links is taken from bs docs:
            # https://www.crummy.com/software/BeautifulSoup/bs4/doc/
            found_links = soup.find_all("a")
            for link in found_links:
                local_links.add(link.get("href"))
            return local_links
        except Exception as e:
            self.logger.log_error(f"crawling {url} failed with {e}")

    def _validate_url(self, url):
        # Take care of http start case
        if not url.startswith("https://"):
            url = "https://" + url
        # Cutting last / to handle relative paths later
        # Otheerwise it shouldn't affect anything
        if url.endswith("/"):
            url = url[:-1]
        # Unless it's a real error, pretend that url is valid
        # Could have been done with regex, to be ~faster, however somewhat less reliable and more complicated to read
        if requests.head(url).status_code < 400:
            return url
        return None

    def _next_url_to_check(self):
        if len(self.urls_to_visit) > 0:
            url = self.urls_to_visit.pop()
            return self._validate_url(url)
        return None

    def _add_new_links_to_visit(self, found_links):
        root_url = self.initial_url
        for next_link in found_links:
            if next_link is None or len(next_link) == 0:
                self.logger.log_error("Link not found in href tag")
                continue
            # assuming this is relative link
            if next_link.startswith("/"):
                next_link = root_url + next_link
            # If we're still in the same domain and haven't visited this link yet
            if next_link.startswith(root_url) and next_link not in self.visited_urls:
                self.urls_to_visit.add(next_link)
