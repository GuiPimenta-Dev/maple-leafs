import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector
from scrapy.utils.project import get_project_settings


class EditorInLeafSpider(scrapy.Spider):
    name = "editor-in-leaf"

    def start_requests(self):
        yield scrapy.FormRequest(
            "https://editorinleaf.com/wp-admin/admin-ajax.php",
            formdata={
                "action": "infinite_scroll",
                "type": "Story_Card_Single",
                "layout": "twocol",
                "post_count": "5000",
            },
            callback=self.parse,
        )

    def parse(self, response):
        response = Selector(text=response.json()["html"])
        divs = response.xpath("//div[@class='layout single twocol']")
        for div in divs:
            url = div.xpath(".//h3/a/@href").get()
            yield scrapy.Request(url, callback=self.parse_article)

    def parse_article(self, response):
        date = response.xpath("//time/@datetime").get().split(" ")[0]
        title = response.xpath("//h1/text()").get()
        author = response.xpath("//a[@class='auth-name']/text()").get()
        if self.keyword.lower() in response.text.lower():
            yield {
                "title": title,
                "author": author,
                "url": response.url,
                "date": date,
            }


# process = CrawlerProcess(get_project_settings())
# process.crawl(EditorInLeafSpider)
# process.start("")
