from datetime import datetime

import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


class GlobalNewsSpider(scrapy.Spider):
    name = "global-news"
    start_urls = ["https://globalnews.ca/tag/nhl/"]

    def parse(self, response):
        lis = response.xpath("//ul[@id='archive-latestStories']//li")

        for li in lis:
            url = response.urljoin(li.xpath(".//a/@href").get())
            title = li.xpath(".//span[@class='c-posts__headlineText']/text()").get()
            yield response.follow(
                url=url, callback=self.parse_article, meta={"title": title}
            )

    def parse_article(self, response):
        author = (
            response.xpath(".//div[@class='c-byline__attribution']//span/text()")
            .get()
            .replace("By ", "")
            .strip()
            or response.xpath(".//div[@class='c-byline__attribution']//a/text()")
            .get()
            .replace("By ", "")
            .strip()
        )

        date = response.xpath(
            '//div[@class="c-byline__date c-byline__date--pubDate"]//span/text()'
        ).get()
        if date:
            date = self.convert_date(date.split("Posted ")[1])

        if self.keyword.lower() in response.text.lower():
            yield {
                "title": response.meta["title"],
                "author": author,
                "url": response.url,
                "date": date,
            }

    @staticmethod
    def convert_date(date_string):
        datetime_obj = datetime.strptime(date_string, "%B %d, %Y %I:%M %p")
        formatted_date = datetime_obj.strftime("%Y-%m-%d")
        return formatted_date


# args = {"keyword": "Maple Leafs"}
# process = CrawlerProcess(get_project_settings())
# process.crawl(GlobalNewsSpider, **args)
# process.start("")
