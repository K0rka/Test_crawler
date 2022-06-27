from src.utils.logger import Logger
from src.utils.crawler import Crawler

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


if __name__ == "__main__":
    handler("monzo.com")
