import csv
from bs4 import BeautifulSoup

import scrapy

class QuotesSpider(scrapy.Spider):
    name = "statcan"
    stat_list = []

    def build_url(self, page):
        return "https://www150.statcan.gc.ca/n1/en/type/data?count=100&p=" + str(page) + "-All#all"

    def start_requests(self):
        max_page = 115
        for page in range(0, max_page + 1):
            url = self.build_url(page)
            print("Start parsing: " + url)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        items = response.css("li.ndm-item")
        for item in items:
            data = self.parse_item(item)
            self.stat_list.append(data)

    def parse_item(self, item):
        # Extract data from the 'item' using BeautifulSoup
        soup = BeautifulSoup(item.get(), "html.parser")

        title = soup.select_one("div.ndm-result-title a").text.strip()
        url = soup.select_one("div.ndm-result-title a")["href"]
        type = soup.select_one("div.ndm-result-productid span").text.strip()
        product_id = soup.select_one("div.ndm-result-productid").contents[1].text.strip()

        freq = ''
        if(soup.select_one("div.ndm-result-freq") != None):
            freq = soup.select_one("div.ndm-result-freq").contents[1].text.strip()

        # Extract the description (handle the case when description is missing)
        description = soup.select_one('div.ndm-result-description').contents[1].text.strip()

        if(description == ''):
            description = soup.select_one('div.ndm-result-description').contents[2].text.strip()

        release_date = soup.select_one("div.ndm-result-date span.ndm-result-date").text.strip()
        
        data = {
            'title': title,
            'url': url,
            'type': type,
            'freq': freq,
            'product_id': product_id,
            'description': description,
            'release_date': release_date,
        }
        return data

    def closed(self, reason):
        # This method is called when the spider is closed (after crawling finishes)
        # Access the 'self.crawler.stats' dictionary to get stats about the crawl (optional)
        # Save the data to a CSV file
        self.save_to_csv()

    def save_to_csv(self):
        # Load the list of items from the spider's 'items' attribute
        data_list = [item for item in self.stat_list]

        # Specify the field names for the CSV file
        field_names = ['title', 'url', 'type', 'freq', 'product_id', 'description', 'release_date']

        # Write the data to a CSV file
        with open('statcan_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=field_names)
            writer.writeheader()
            writer.writerows(data_list)
