import datetime
import urllib.parse

import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


class TheScoreSpider(scrapy.Spider):
    name = "the-score"

    def start_requests(self):
        base_url = "https://rich-content.thescore.com/content_cards"
        parameters = {
            "resource_uris": "/maple-leafs/leagues/1",
            "limit": 50,
            "before": datetime.datetime.now(datetime.timezone.utc).strftime(
                "%Y-%m-%dT%H:%M:%S.000Z"
            ),
            "exclude_pinned": True,
            "card_types": "InstagramVideoCard,SourcedArticleCard,theScoreArticleCard,TwitterAnimatedGifCard,TwitterVideoCard,TwitterVideoStreamCard,YoutubeVideoCard",
        }
        url = f"{base_url}?{urllib.parse.urlencode(parameters)}"
        yield scrapy.Request(
            url=url,
            callback=self.parse,
        )

    def parse(self, response):
        cards = response.json()["content_cards"]
        for card in cards:
            content = card["data"].get("content")
            if content and self.keyword.lower() in content.lower():
                url = card["data"].get("share_url")
                author = card["data"]["byline"]
                title = card["data"]["title"]
                date = card["published_at"].split("T")[0]
                yield {
                    "title": title,
                    "url": url,
                    "date": date,
                    "author": author,
                }


# args = {"keyword": "Maple Leafs"}
# process = CrawlerProcess(get_project_settings())
# process.crawl(TheScoreSpider, **args)
# process.start("")
