from urllib.parse import urlencode

import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


class TheGlobeAndMailSpider(scrapy.Spider):
    name = "the-globe-and-mail"
    start = 0
    size = 100
    url = (
        'https://www.theglobeandmail.com/pf/api/v3/content/fetch/content-search?query={"contentQuery":"taxonomy.sites.path:/sports/maple-leafs","from":'
        + str(start)
        + ',"size":'
        + str(size)
        + ',"sort":"display_date:desc"}'
    )

    def start_requests(self):
        yield scrapy.Request(
            url=self.url,
            callback=self.parse,
        )

    def parse(self, response):
        elements = response.json()["content_elements"]
        for element in elements:
            title = element["headlines"]["basic"]
            url = "https://www.theglobeandmail.com" + element["canonical_url"]
            date = element["publish_date"].split("T")[0]
            author = element["credits"]["by"]
            author = author[0]["name"] if author else None
            yield scrapy.Request(
                url=url,
                callback=self.parse_article,
                meta={"title": title, "date": date, "author": author},
            )

    def parse_article(self, response):
        author = (
            response.meta["author"]
            or response.xpath("//span[@class='c-creditline text-gmr-5']/text()").get()
        )
        if self.keyword.lower() in response.text.lower():
            yield {
                "title": response.meta["title"],
                "date": response.meta["date"],
                "author": author,
                "url": response.url,
            }


# process = CrawlerProcess(get_project_settings())
# process.crawl(TheGlobeAndMailSpider)
# process.start("")
