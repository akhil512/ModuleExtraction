import asyncio
import logging
from requests_html import AsyncHTMLSession
from Tools.web_scraper import WebScraper
from urllib.parse import urlparse

logging.basicConfig(level=logging.INFO)

class WebCrawler:
    def __init__(self, url, max_depth=1):
        self.url = url
        self.max_depth = max_depth
        self.visited = set()
        self.results = {
            "parent_link": None,
            "child_links": []
        }

    async def crawl(self, url=None, depth=0, session=None):
        # Main crawling logic with error handling
        if url is None:
            url = self.url
        if url in self.visited or depth > self.max_depth:
            return
        self.visited.add(url)
        try:
            base_domain = urlparse(self.url).netloc
            current_domain = urlparse(url).netloc
            if current_domain == base_domain:
                logging.info(f"Crawling: {url}")
                try:
                    scraper = WebScraper(url)
                    content = await scraper.get_text()
                    if url == self.url:
                        self.results["parent_link"] = {"url": url, "text": content}
                    else:
                        self.results["child_links"].append({"url": url, "text": content})
                except Exception as scrape_err:
                    logging.error(f"Error scraping {url}: {scrape_err}")
            try:
                r = await session.get(url)
                tasks = []
                for link in r.html.absolute_links:
                    if 'tiktok.com' not in link:
                        tasks.append(self.crawl(link, depth + 1, session))
                await asyncio.gather(*tasks)
            except Exception as crawl_links_err:
                logging.error(f"Error crawling links from {url}: {crawl_links_err}")
        except Exception as e:
            logging.error(f"Failed to crawl {url}: {e}")

    async def start(self):
        # Entry point for the crawler with error handling
        try:
            session = AsyncHTMLSession()
            await self.crawl(session=session)
            await session.close()
            return self.results
        except Exception as e:
            logging.error(f"Crawler failed to start: {e}")
            return self.results

# Example usage:
# if __name__ == "__main__":
#     url = input("Enter the URL to crawl: ")
#     max_depth = int(input("Enter max crawl depth: "))
#     crawler = WebCrawler(url, max_depth)
#     results = asyncio.run(crawler.start())
#     import json
#     print(json.dumps(results, indent=2))