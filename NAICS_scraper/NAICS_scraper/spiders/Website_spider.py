import scrapy
from ..items import NaicsScraperItem
import re
from pymongo import MongoClient


def getURL():
    client = MongoClient('mongodb://localhost:27017')
    collection = 'NAICS_DB'
    db = client[collection]
    table_NAICS = db['db_test']
    results = table_NAICS.find({}, {'URL': 1, '_id': 0})
    results = list(results)
    return results


class Website_Spider(scrapy.Spider):
    name = "websites"
    allowed_domains = ['']

    def __init__(self, *args, **kwargs):
        super(Website_Spider, self).__init__(*args, **kwargs)
        self.counter = 0
        self.start_urls = []
        URL_dict = getURL()
        for url in URL_dict:
            if url["URL"] != "":
                print(url["URL"])
                self.start_urls.append("http://" + url["URL"])

    # def parse(self, response):
    #     original_url = response.request.url
    #     results = response.xpath("//a/*[contains(text(), 'Learn More')]").getall()
    #     print(results, original_url)

    def parse(self, response):
        original_url = response.request.url
        results = ''.join(response.xpath("//body//text()").extract()).strip()
        print(results, original_url)

