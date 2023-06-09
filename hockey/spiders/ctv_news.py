from datetime import datetime

import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


class CtvNewsSpider(scrapy.Spider):
    name = "ctv-news"
    start_urls = ["https://www.ctvnews.ca/sports"]

    def parse(self, response):
        lis = response.xpath("//li[@class='c-list__item']")
        for li in lis:
            date = li.xpath(".//h3//span/@data-published-date").get()
            if date:
                date = date.strip().split(" ")
                dates = [date[1], date[2], date[-1]]
                date = self.parse_date(" ".join(dates))
            title = li.xpath(".//a/text()").get().strip()
            url = li.xpath(".//a/@href").get().strip()

            yield response.follow(
                url=url,
                callback=self.parse_article,
                meta={"title": title, "date": date},
            )

    def parse_article(self, response):
        if self.keyword.lower() in response.text.lower():
            yield {
                "title": response.meta["title"],
                "author": "Staff",
                "url": response.url,
                "date": response.meta["date"],
            }

    @staticmethod
    def parse_date(date_string):
        parsed_date = datetime.strptime(date_string, "%b %d %Y")
        formatted_date = parsed_date.strftime("%Y-%m-%d")
        return formatted_date


# args = {"keyword": "Maple Leafs"}
# process = CrawlerProcess(get_project_settings())
# process.crawl(CtvNewsSpider, **args)
# process.start("")
