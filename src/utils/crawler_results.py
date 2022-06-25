# Class which is responsible for storing results of crawling in an expected format
# In real life it could be storage of any kind (cache/db/s3), or passing it to next service
class CrowlerResult:
    results = {}

    def __init__(self, logger):
        self.logger = logger

    def add_results(self, main_url, found_links):
        self.results[main_url] = found_links
        self._save_results(main_url, found_links)

    def _save_results(self, main_url, found_links):
        print(main_url)
        for next_ in found_links:
            print(f"\t{next_}")
