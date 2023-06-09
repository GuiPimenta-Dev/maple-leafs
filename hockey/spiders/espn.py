import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from urllib.parse import urlencode


class EspnSpider(scrapy.Spider):
    name = "espn"

    def start_requests(self):
        params = {
            "offset": 0,
            "limit": 15,
            "lang": "en",
            "authorizedNetworks": "espn_free",
            "editionKey": "espn-en",
            "device": "desktop",
            "pubkey": "espn-en-nhl-index",
            "isPremium": "true",
            "locale": "br",
            "featureFlags": [
                "expandAthlete",
                "mmaGB",
                "enhancedGameblock",
                "watchRowLeagueAiring",
                "overrideMetadata",
            ],
            "showAirings": "buy,live",
        }
        base_url = "https://onefeed.fan.api.espn.com/apis/v3/cached/contentEngine/oneFeed/leagues/nhl?"
        url = base_url + urlencode(params)
        yield scrapy.Request(
            url=url,
            callback=self.parse,
        )

    def parse(self, response):
        feed = response.json()["feed"]
        for item in feed:
            title = item["data"]["now"][0]["headline"]
            url = item["data"]["now"][0].get("links")
            if url:
                url = url["web"]["href"]
            else:
                continue
            date = item["data"]["now"][0]["published"].split("T")[0]
            author = item["data"]["now"][0].get("byline")
            yield scrapy.Request(
                url=url,
                callback=self.parse_article,
                meta={"title": title, "date": date, "author": author},
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
# process.crawl(EspnSpider, **args)
# process.start("")
