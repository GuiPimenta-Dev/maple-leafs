from datetime import datetime, timedelta

import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


class TorontosunSpider(scrapy.Spider):
    name = "torontosun"
    start_urls = [
        f"https://torontosun.com/category/sports/hockey/nhl/toronto-maple-leafs"
    ]

    def parse(self, response):
        articles = response.xpath("//article[@data-category-colour='sports']")

        for article in articles:
            url = response.urljoin(article.xpath(".//a/@href").get())
            title = article.xpath(".//a/@aria-label").get()
            yield response.follow(
                url=url, callback=self.parse_article, meta={"title": title}
            )

    def parse_article(self, response):
        date = response.xpath(".//span[@class='published-date__since']/text()").get()
        if date:
            date = date.split("Published ")[1]
            date = self.format_date_string(date)
        author = (
            response.xpath(".//span[@class='published-by__author']//a/text()").get()
            or response.xpath(".//span[@class='published-by__author']/text()").get()
            or response.xpath(".//div[@id='wire-company-name']/text()").get()
        )

        if self.keyword.lower() in response.text.lower():
            yield {
                "title": response.meta["title"],
                "author": author.strip() if author else None,
                "url": response.url,
                "date": date,
            }

    @staticmethod
    def format_date_string(date_string):
        date = datetime.strptime(date_string, "%b %d, %Y")
        formatted_date = date.strftime("%Y-%m-%d")
        return formatted_date


# process = CrawlerProcess(get_project_settings())
# process.crawl(TorontosunSpider)
# process.start("")
