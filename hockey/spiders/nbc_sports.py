import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


class NbcSportsSpider(scrapy.Spider):
    name = "nbc-sports"
    start_urls = ["https://www.nbcsportsedge.com/"]

    def parse(self, response):
        links = response.xpath("//a[@rel='bookmark']")
        for link in links:
            url = link.xpath("./@href").get()
            title = response.xpath("//a[@rel='bookmark']//span/text()").get()
            yield response.follow(
                url=url, callback=self.parse_article, meta={"title": title}
            )

    def parse_article(self, response):
        author = response.xpath(
            "//span[@class='article-full__author-name article-full__author-name--header']/text()"
        ).get()
        if author:
            author = author.replace("by ", "").strip()
        date = response.xpath("//time/@datetime").get()
        if date:
            date = date.split("T")[0]

        if self.keyword.lower() in response.text.lower():
            yield {
                "title": response.meta["title"],
                "author": author,
                "date": date,
                "url": response.url,
            }


# args = {"keyword": "Maple Leafs"}
# process = CrawlerProcess(get_project_settings())
# process.crawl(NbcSportsSpider, **args)
# process.start("")
