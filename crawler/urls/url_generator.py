import asyncio
import logging

from crawler.urls.google_query import get_google_query
from crawler.proxies.proxy import get_working_proxy
from crawler.exceptions.crawl_exception import CrawlException
from paths.paths import urls_path

from crawl4ai import AsyncWebCrawler
from crawl4ai.async_configs import BrowserConfig, CrawlerRunConfig


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def get_urls(user_query: str, max_retries: int = 3, delay: int = 2):
    """
    Get URLs with retry logic and improved error handling
    """
    query = get_google_query(user_query)
    print(f"Google Query: {query}")
    
    for attempt in range(max_retries):
        try:
            # Get a fresh proxy for each attempt
            proxy = get_working_proxy(query)
            logger.info(f"Attempt {attempt + 1}/{max_retries} using proxy: {proxy}")
            
            browser_config = BrowserConfig(
                headless=True,
                proxy=proxy,
                # ignore_https_errors=True,
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

            # Increase timeout and adjust wait conditions
            crawler_config = CrawlerRunConfig(
                page_timeout=30000,  # 30 seconds
                wait_until="networkidle",  # Wait until network is idle
                delay_before_return_html=2.0,  # Wait 2 seconds before returning
            )

            async with AsyncWebCrawler(config=browser_config) as crawler:
                result = await crawler.arun(
                    url=query,
                    config=crawler_config
                )
                
                # Check if the crawl was successful
                if result.success:  # type: ignore
                    logger.info("Successfully crawled the URL")
                    return result
                else:
                    logger.warning(f"Crawl failed: {result.error_message}")  # type: ignore
                    if attempt == max_retries - 1:
                        raise CrawlException(f"All attempts failed. Last error: {result.error_message}") # type: ignore
                    
        except asyncio.TimeoutError as e:
            logger.warning(f"Timeout error on attempt {attempt + 1}: {e}")
            if attempt == max_retries - 1:
                raise CrawlException(f"Timeout after {max_retries} attempts")
                
        except RuntimeError as e:
            logger.warning(f"Runtime error on attempt {attempt + 1}: {e}")
            if attempt == max_retries - 1:
                raise CrawlException(f"Runtime error after {max_retries} attempts: {e}")
                
        except Exception as e:
            logger.error(f"Unexpected error on attempt {attempt + 1}: {e}")
            if attempt == max_retries - 1:
                raise CrawlException(f"Unexpected error after {max_retries} attempts: {e}")
        
        if attempt < max_retries - 1:
            # delay = base_delay * (2 ** attempt) + (asyncio.get_event_loop().time() % 1)
            logger.info(f"Waiting {delay:.2f} seconds before retry...")
            await asyncio.sleep(delay)
    
    raise CrawlException(f"Failed to get URLs after {max_retries} attempts")

                


async def generate_urls(user_query: str):
    result = await get_urls(user_query, max_retries=10)
    if result.success: # type: ignore
        with open(urls_path, "w", encoding="utf-8") as f:
            for link in result.links["external"]:  # type: ignore
                f.write(f"{link["href"]}\n")

# if __name__ == "__main__":
#     asyncio.run(main())
    
