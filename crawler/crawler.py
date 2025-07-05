import asyncio
import logging
from crawl4ai import AsyncWebCrawler
from crawl4ai.async_configs import BrowserConfig, CrawlerRunConfig, CacheMode
from crawl4ai.async_dispatcher import MemoryAdaptiveDispatcher

from crawler.proxies.proxy import get_working_proxy
from crawler.urls.url_generator import generate_urls
from paths.paths import crawled_websites_path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def parallel_crawler(query: str, max_concurrency: int = 10):

    await generate_urls(query)
    crawler_config = CrawlerRunConfig(
        cache_mode=CacheMode.BYPASS, 
        page_timeout=30000,  # 30 seconds
        wait_until="networkidle",  # Wait until network is idle
        delay_before_return_html=2.0,  # Wait 2 seconds before returning
        stream=False
    )
    
    dispatcher = MemoryAdaptiveDispatcher(
        memory_threshold_percent=70.0,
        check_interval=1.0,
        max_session_permit=max_concurrency
    )

    urls_path = "/mnt/1670554E70553629/Python-Comding/Reasearch Assistant/crawler/urls/urls.txt"

    with open(urls_path, "r") as f:
        urls = f.read().split("\n")

        try:
            proxy = get_working_proxy("https://ipinfo.io/json")
            logger.info(f"using proxy: {proxy}")

            browser_config = BrowserConfig(
                headless=True,
                verbose=False,
                extra_args=[
                    "--no-sandbox",
                    "--disable-setuid-sandbox",
                    "--disable-dev-shm-usage",
                    "--disable-blink-features=AutomationControlled",
                    "--disable-extensions",
                    "--disable-plugins",
                    "--disable-images",  # Speed up loading
                ]
            )



            async with AsyncWebCrawler(config=browser_config) as crawler:
                results = await crawler.arun_many(
                    urls = urls,
                    config=crawler_config,
                    dispatcher=dispatcher
                )
                with open(crawled_websites_path, "w", encoding="utf-8") as f:
                    for result in results:  # type: ignore
                        if result.success:  # type: ignore
                            logger.info("Successfully crawled the URL")
                            f.write(result.markdown)
                        else:
                            logger.warning(f"Crawl failed: {result.error_message}")  # type: ignore
                            # f.write(f"Error Crawling: {result.url} : {result.error_message}")
                            # raise CrawlException(f"Last error: {result.error_message}") # type: ignore
        except asyncio.TimeoutError as e:
            logger.error(f"Unexpected error: {e}")
            # raise CrawlException(f"Unexpected error {e}")

                
        except RuntimeError as e:
            logger.error(f"Unexpected error: {e}")
            # raise CrawlException(f"Unexpected error {e}")
                
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            # raise CrawlException(f"Unexpected error {e}")

                
            
# if __name__ == "__main__":
#     asyncio.run(parallel_crawler())
