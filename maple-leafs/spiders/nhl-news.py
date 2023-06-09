import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


class NhlNewsSpider(scrapy.Spider):
    name = "nhl-news"
    start_urls = [
        "https://www.nhl.com/mapleleafs/news/search-articles?page=1&tid=277350296"
    ]

    def parse(self, response):
        articles = response.xpath("//article")

        for article in articles:
            title = article.xpath(".//@data-title").get()
            author = article.xpath(".//@data-author").get()
            url = response.urljoin(article.xpath(".//@data-url").get())
            date = article.xpath(".//@data-pub-date").get().split("T")[0]

            if self.keyword.lower() in response.text.lower():
                yield {"title": title, "author": author, "url": url, "date": date}


# process = CrawlerProcess(get_project_settings())
# process.crawl(NhlNewsSpider)
# process.start("")
