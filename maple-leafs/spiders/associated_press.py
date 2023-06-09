import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


class AssociatedPressSpider(scrapy.Spider):
    name = "associated-press"
    start_urls = ["https://apnews.com/hub/nhl"]

    def parse(self, response):
        divs = response.xpath('//div[contains(@class, "FeedCard")]')
        for div in divs:
            url = div.xpath(".//a/@href").get()
            title = div.xpath(".//h2/text()").get()
            author = div.xpath(
                './/span[contains(@class, "Component-bylines")]/text()'
            ).get()
            if author:
                author = author.split("By ")[1]
            date = (
                div.xpath('.//span[@data-key="timestamp"]/@data-source')
                .get()
                .split("T")[0]
            )
            yield response.follow(
                url=url,
                callback=self.parse_article,
                meta={"title": title, "author": author, "date": date},
            )

    def parse_article(self, response):
        if self.keyword.lower() in response.text.lower():
            yield {
                "title": response.meta["title"],
                "author": response.meta["author"],
                "date": response.meta["date"],
                "url": response.url,
            }


# args = {"keyword": "Maple Leafs"}
# process = CrawlerProcess(get_project_settings())
# process.crawl(AssociatedPressSpider, **args)
# process.start("")
