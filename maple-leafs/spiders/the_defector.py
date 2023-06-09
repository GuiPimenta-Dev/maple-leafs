import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


class TheDefectorSpider(scrapy.Spider):
    name = "the-defector"

    def start_requests(self):
        url = (
            "https://defector.com/_next/data/znCrRntjnndntM8I6fSWC/en/category/nhl.json"
        )
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        posts = response.json()["pageProps"]["posts"]
        for post in posts:
            title = post["title"]
            url = post["link"]
            date = post["modifiedGmt"].split("T")[0]
            author = post["byline"]["profiles"]
            if author:
                author = author[0]["title"]

            yield scrapy.Request(
                url=url,
                callback=self.parse_article,
                meta={"title": title, "date": date, "author": author},
            )

    def parse_article(self, response):
        if self.keyword.lower() in response.text.lower():
            yield {
                "title": response.meta["title"],
                "author": response.meta["author"],
                "url": response.url,
                "date": response.meta["date"],
            }


# args = {"keyword": "Maple Leafs"}
# process = CrawlerProcess(get_project_settings())
# process.crawl(TheDefectorSpider, **args)
# process.start("")
