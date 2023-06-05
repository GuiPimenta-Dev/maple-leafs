import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


class TheLeafsNationSpider(scrapy.Spider):
    name = "the-leafs-nation"

    def start_requests(self):
        url = "https://theleafsnation.com/_next/data/1kqlqAof1lLxAqQyKF1Ya/en/category/news.json"  # Replace with the URL you want to request
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        edges = response.json()["pageProps"]["posts"]["edges"]
        for edge in edges:
            title = edge["node"]["title"]
            slug = edge["node"]["slug"]
            author = edge["node"]["author"]["node"]["name"]
            date = edge["node"]["dateGmt"].split("T")[0]

            url = f"https://theleafsnation.com/_next/data/1kqlqAof1lLxAqQyKF1Ya/en/news/{slug}.json?slug={slug}"
            link = f"https://theleafsnation.com/news/{slug}"
            yield response.follow(
                url=url,
                callback=self.parse_article,
                meta={"title": title, "url": link, "author": author, "date": date},
            )

    def parse_article(self, response):
        post = response.json()["pageProps"]["posts"][0]
        raw_content = post["raw_content"].lower()
        title = response.meta["title"]
        url = response.meta["url"]
        author = response.meta["author"]
        if self.keyword.lower() in raw_content or self.keyword in title.lower():
            yield {
                "title": title,
                "url": url,
                "author": author,
                "date": response.meta["date"],
            }


# process = CrawlerProcess(get_project_settings())
# process.crawl(TheLeafsNationSpider)
# process.start("")
