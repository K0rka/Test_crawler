from src.utils.logger import Logger
from src.utils.crawler import Crawler
import sys

logger = Logger()


# Print all visited with list of links on them
def handler(url):
    logger.log_info(f"Start crawling with {url}")

    try:
        crawler = Crawler(url, logger)
        crawler.crawl()
    except Exception as e:
        logger.log_metric("process_failed", 1)
        logger.log_error(f"Failed with {e}")
    else:
        logger.log_metric("process_succeeded", 1)
    finally:
        logger.log_info(f"Finished crawling for {url}")

# This is only testing support,
# For that reason for now handling command line arguments is like this
if __name__ == "__main__":
    args = sys.argv
    # args[0] = current file
    # args[1] = url if exists
    url = "monzo.com"
    if len(args) >= 2:
        url = args[1]

    handler(url)
