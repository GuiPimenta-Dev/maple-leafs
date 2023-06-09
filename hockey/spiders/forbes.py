import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import urllib.parse
import datetime


class ForbesSpider(scrapy.Spider):
    name = "forbes"

    def start_requests(self):
        base_url = "https://www.forbes.com/simple-data/chansec/stream"
        parameters = {
            "start": 0,
            "ids": "content_647ef95a57c0792cdf2ca770",
            "sourceValue": "channel_1section_5",
            "swimLane": "",
            "specialSlot": "sports-money",
            "streamSourceType": "channelsection",
        }
        url = f"{base_url}?{urllib.parse.urlencode(parameters)}"
        yield scrapy.Request(
            url=url,
            callback=self.parse,
        )

    def parse(self, response):
        items = response.json()["blocks"]["items"]
        for item in items:
            author = item["author"].get("name")
            title = item["title"]
            ms_date = item["date"] / 1000
            date = datetime.datetime.fromtimestamp(ms_date).strftime("%Y-%m-%d")
            url = item["url"]

            yield scrapy.Request(
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
# process.crawl(ForbesSpider, **args)
# process.start("")
