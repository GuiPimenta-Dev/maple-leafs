from datetime import datetime, timedelta

import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


class NhlpaSpider(scrapy.Spider):
    name = "nhlpa"
    start_urls = ["https://www.nhlpa.com/news"]
    page = 1

    def parse(self, response):
        rows = response.xpath("//a[@class='result row']")

        for row in rows:
            try:
                url = response.urljoin(row.xpath(".//@href").get())
                author = (
                    row.xpath(".//div[@class='author']/text()")
                    .get()
                    .split("By:")[1]
                    .strip()
                )
                title = row.xpath(".//h4/text()").get().strip()
                date = row.xpath(".//span/text()").getall()[-1].strip()
                if "ago" in date:
                    date = self.get_date_from_time_delta(date)
                else:
                    date = self.get_date_from_string(date)

                yield {
                    "title": title,
                    "author": author,
                    "url": url,
                    "date": date,
                }
            except Exception as e:
                print(e)

        if rows:
            self.page += 1
            next_page = f"https://www.nhlpa.com/news?page={self.page}"
            yield scrapy.Request(next_page, callback=self.parse)

    @staticmethod
    def get_date_from_time_delta(time_delta):
        current_date = datetime.now().date()
        number = time_delta.split(" ")[0]
        number = int(number)
        delta = timedelta(days=number)
        desired_date = current_date - delta
        formatted_date = desired_date.strftime("%Y-%m-%d")
        return formatted_date

    @staticmethod
    def get_date_from_string(date_string):
        date = datetime.strptime(date_string, "%B %d, %Y")
        formatted_date = date.strftime("%Y-%m-%d")
        return formatted_date


# process = CrawlerProcess(get_project_settings())
# process.crawl(NhlpaSpider)
# process.start("")
