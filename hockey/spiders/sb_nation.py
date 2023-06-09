import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


class SbNationSpider(scrapy.Spider):
    name = "sb-nation"
    start_urls = ["https://www.sbnation.com/nhl"]

    def parse(self, response):
        divs = response.xpath("//div[@class='c-compact-river__entry ']")
        for div in divs:
            url = div.xpath(".//a/@href").get()
            title = div.xpath(".//h2/a/text()").get()
            author = div.xpath(".//span[@class='c-byline__author-name']/text()").get()
            date = div.xpath(".//time/@datetime").get()
            if date:
                date = date.split("T")[0]

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
# process.crawl(SbNationSpider, **args)
# process.start("")
