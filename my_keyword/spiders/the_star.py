from datetime import datetime

import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


class TheStarSpider(scrapy.Spider):
    name = "the-star"
    page = 1
    start_urls = ["https://www.thestar.com/sports/leafs.html"]

    def parse(self, response):
        links = response.xpath(
            "//div[@class='c-fixed-articlelist-container__content']//a"
        )

        for link in links:
            url = response.urljoin(link.xpath(".//@href").get())
            title = link.xpath(
                ".//span[@data-test-id='mediacard-headline']/text()"
            ).get()

            yield response.follow(
                url, callback=self.parse_article, meta={"title": title}
            )

    def parse_article(self, response, **kwargs):
        author = response.xpath("//span[@class='article__author-credit']/text()").get()
        date = self.format_date(
            response.xpath("//span[@class='article__published-date']/text()").get()
        )
        if self.keyword.lower() in response.text.lower():
            yield {
                "title": response.meta["title"],
                "author": author,
                "url": response.url,
                "date": date,
            }

    @staticmethod
    def format_date(date_string):
        date_obj = datetime.strptime(date_string, "%a., %B %d, %Y")
        formatted_date = date_obj.strftime("%Y-%m-%d")
        return formatted_date


# process = CrawlerProcess(get_project_settings())
# process.crawl(NhlSpider)
# process.start("")
