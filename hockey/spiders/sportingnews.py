import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


class SportingnewsSpider(scrapy.Spider):
    name = "sportingnews"
    start_urls = ["https://www.sportingnews.com/ca/nhl/news"]

    def parse(self, response):
        divs = response.xpath("//div[@role='article']")
        for div in divs:
            url = div.xpath(".//@about").get()
            title = div.xpath(".//@content").get()
            yield response.follow(
                url=url, callback=self.parse_article, meta={"title": title}
            )

    def parse_article(self, response):
        author = response.xpath("//a[@class='author-name__link']/text()").get()
        date = response.xpath("//time/@datetime").get().split("T")[0]
        if self.keyword.lower() in response.text.lower():
            yield {
                "title": response.meta["title"],
                "author": author,
                "date": date,
                "url": response.url,
            }


# args = {"keyword": "Maple Leafs"}
# process = CrawlerProcess(get_project_settings())
# process.crawl(SportingnewsSpider, **args)
# process.start("")
