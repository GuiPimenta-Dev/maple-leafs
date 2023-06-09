from datetime import datetime, timedelta
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


class BleacherReportSpider(scrapy.Spider):
    name = "bleacher-report"
    start_urls = ["https://bleacherreport.com/nhl"]

    def parse(self, response):
        lis = response.xpath("//li[@class='cell articleSummary']")
        for li in lis:
            url = li.xpath(".//a/@href").get()
            yield response.follow(
                url=url,
                callback=self.parse_article,
            )

    def parse_article(self, response):
        title = response.xpath(".//h1/text()").get()
        author = response.xpath(".//span[@class='name']/text()").get()
        date = response.xpath(".//span[@class='date']/text()").get()
        if date:
            date = self.parse_date(date)

        if self.keyword.lower() in response.text.lower():
            yield {
                "title": title,
                "author": author,
                "date": date,
                "url": response.url,
            }

    @staticmethod
    def parse_date(date_string):
        date = datetime.strptime(date_string, "%B %d, %Y")
        formatted_date = date.strftime("%Y-%m-%d")
        return formatted_date


# args = {"keyword": "Maple Leafs"}
# process = CrawlerProcess(get_project_settings())
# process.crawl(BleacherReportSpider, **args)
# process.start("")
