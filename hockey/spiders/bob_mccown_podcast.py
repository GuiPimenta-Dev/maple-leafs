from datetime import datetime

import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


class BobMccownPodcastSpider(scrapy.Spider):
    name = "bob-mccown-podcast"
    start_urls = ["https://mapleleafsaggr.com/src/bob-mccown-podcast"]

    def parse(self, response):
        articles = response.xpath("//article")
        for article in articles:
            title = article.xpath(".//h3//a/text()").get()
            url = response.urljoin(article.xpath(".//h3//a/@href").get())
            author = article.xpath(".//p//a/text()").get()
            date = article.xpath(".//a[@class='post-date']/text()").get()
            date = self.format_date(date)

            yield {
                "title": title,
                "author": author,
                "url": url,
                "date": date,
            }

    @staticmethod
    def format_date(date_str):
        date_str_with_year = f"{date_str}, {datetime.now().year}"
        datetime_obj = datetime.strptime(date_str_with_year, "%b %d, %I:%M %p, %Y")
        formatted_date = datetime_obj.strftime("%Y-%m-%d")
        return formatted_date


# args = {"keyword": "Maple Leafs"}
# process = CrawlerProcess(get_project_settings())
# process.crawl(BobMccownPodcastSpider, **args)
# process.start("")
