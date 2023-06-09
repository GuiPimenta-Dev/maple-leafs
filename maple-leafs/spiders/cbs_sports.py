import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


class CbsSportsSpider(scrapy.Spider):
    name = "cbs-sports"
    start_urls = ["https://www.cbssports.com/nhl/"]

    def parse(self, response):
        divs = response.xpath("//div[@class='article-list-marquee-item dek-slide-in']")
        for div in divs:
            url = div.xpath(".//a/@href").get()
            title = div.xpath(".//a/@aria-label").get()
            yield response.follow(
                url=url, callback=self.parse_article, meta={"title": title}
            )

        lis = response.xpath("//ul[@class='row article-list-pack-row ']//li")
        for li in lis:
            url = li.xpath(".//a/@href").get()
            if url:
                title = li.xpath(".//h5//a/text()").get()
                yield response.follow(
                    url=url, callback=self.parse_article, meta={"title": None}
                )

    def parse_article(self, response):
        author = (
            response.xpath("//a[@rel='author']/text()").get().strip()
            or (
                response.xpath("//a[@class='ArticleAuthor-name--link']/text()")
                .get()
                .strip()
            )
            or (
                response.xpath("//span[@class='ArticleAuthor-nameText']/text()")
                .get()
                .strip()
            )
        )

        date = response.xpath("//time/@datetime").get().split(" ")[0]
        if self.keyword.lower() in response.text.lower():
            yield {
                "title": response.meta["title"],
                "author": author,
                "date": date,
                "url": response.url,
            }


# args = {"keyword": "Maple Leafs"}
# process = CrawlerProcess(get_project_settings())
# process.crawl(CbsSportsSpider, **args)
# process.start("")
