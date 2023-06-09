import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


class CbcSpider(scrapy.Spider):
    name = "cbc"
    start_urls = ["https://www.cbc.ca/sports/maple-leafs/nhl"]

    def parse(self, response):
        links = response.xpath('//a[@data-cy="type-story"]')
        for link in links:
            url = response.urljoin(link.xpath(".//@href").get())
            title = link.xpath(".//text()").get()
            author = link.xpath(".//div[@class='authorName']/text()").get()
            date = link.xpath(".//time/@datetime").get().split("T")[0]
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
# process.crawl(CbcSpider, **args)
# process.start("")
