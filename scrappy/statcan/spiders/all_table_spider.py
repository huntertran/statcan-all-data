from pathlib import Path

import scrapy

class QuotesSpider(scrapy.Spider):
    name = "statcan"

    def build_url(self, page):
        return "https://www150.statcan.gc.ca/n1/en/type/data?count=100&p=" + str(page) + "-All#all"

    def start_requests(self):
        max_page = 3
        for page in range(1, max_page + 1):
            url = self.build_url(page)
            print("Start parsing: " + url)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        items = response.css("li.ndm-item")
        for item in items:
            print(item)
