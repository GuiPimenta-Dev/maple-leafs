import re
from datetime import datetime, timedelta

import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


class TheAthleticSpider(scrapy.Spider):
    name = "the-athletic"
    start_urls = ["https://theathletic.com/uk/"]

    def parse(self, response):
        links = response.xpath(
            "//a[@class='MuiTypography-root MuiLink-root MuiLink-underlineNone MuiTypography-colorInherit']"
        )
        for link in links:
            url = link.xpath(".//@href").get()
            title = link.xpath(".//img/@alt").get()
            yield response.follow(
                url=url, callback=self.parse_article, meta={"title": title}
            )

    def parse_article(self, response):
        author = response.xpath("//u/text()").get()

        date = response.xpath(
            "//div[@class='article-headline']//div//div//div/text()"
        ).get()
        if date:
            if "ago" in date:
                date = self.get_date_from_time_delta(date)
            else:
                date_format = "%b. %d, %Y" if "." in date else "%b %d, %Y"
                date = self.convert_date(date, date_format)

        if self.keyword.lower() in response.text.lower():
            yield {
                "title": response.meta["title"],
                "author": author.strip() if author else None,
                "url": response.url,
                "date": date,
            }

    @staticmethod
    def get_date_from_time_delta(time_delta):
        current_date = datetime.now().date()
        number = time_delta.split(" ")[0]
        number = int(re.sub(r"[^0-9]", "", number))
        delta = timedelta(days=number)
        desired_date = current_date - delta
        formatted_date = desired_date.strftime("%Y-%m-%d")
        return formatted_date

    @staticmethod
    def convert_date(date_str, date_format):
        date_obj = datetime.strptime(date_str, date_format)
        formatted_date = date_obj.strftime("%Y-%m-%d")
        return formatted_date


# args = {"keyword": "Maple Leafs"}
# process = CrawlerProcess(get_project_settings())
# process.crawl(TheAthleticSpider, **args)
# process.start("")
