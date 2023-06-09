import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


class DeadspinSpider(scrapy.Spider):
    name = "deadspin"
    start_urls = ["https://deadspin.com/maple-leafs"]

    def parse(self, response):
        articles = response.xpath("//article")
        for article in articles:
            url = article.xpath(".//a/@href").get()
            title = article.xpath(".//h4/text()").get()
            yield response.follow(
                url=url,
                callback=self.parse_article,
                meta={"title": title},
            )

    def parse_article(self, response):
        author = response.xpath(
            "//div[@class='js_starterpost']//div//div//div//div//div//div//span/text()"
        ).get()
        date = response.xpath("//time/@datetime").get().split("T")[0]

        if self.keyword.lower() in response.text.lower():
            yield {
                "title": response.meta["title"],
                "author": author,
                "url": response.url,
                "date": date,
            }


# args = {"keyword": "Maple Leafs"}
# process = CrawlerProcess(get_project_settings())
# process.crawl(DeadspinSpider, **args)
# process.start("")
