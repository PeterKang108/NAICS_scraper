import scrapy
import nltk
from ..items import NaicsWebsiteItems
import re
from pymongo import MongoClient
from bs4 import BeautifulSoup

from urllib import request
from urllib.request import Request, urlopen
import requests

def getURL():
    client = MongoClient('mongodb://localhost:27017')
    collection = 'NAICS_DB'
    db = client[collection]
    table_NAICS = db['db_test']
    results = table_NAICS.find({}, {'URL': 1, 'NAICS_Code': 1, 'Company_Name': 1, '_id': 0})
    results = list(results)
    return results


class Website_Spider(scrapy.Spider):
    name = "websites"
    allowed_domains = ['']

    def __init__(self, *args, **kwargs):
        super(Website_Spider, self).__init__(*args, **kwargs)
        self.counter = 0
        self.start_urls = []
        self.ObjectDict = getURL()

    # def parse(self, response):
    #     original_url = response.request.url
    #     results = response.xpath("//a/*[contains(text(), 'Learn More')]").getall()
    #     print(results, original_url)

    def start_requests(self):
        for i, entry in enumerate(self.ObjectDict):
            req_https = scrapy.Request('https://' + entry['URL'], callback=self.parse, cb_kwargs={'index': 1})
            yield req_https
            # req_http = scrapy.Request('http://' + entry['URL'], callback=self.parse, cb_kwargs={'index': 1})
            # yield req_http

    def parse(self, response, index):
        item = NaicsWebsiteItems()
        original_url = response.request.url
        request_site = Request(original_url, headers={"User-Agent": "Mozilla/5.0"})
        session_obj = requests.Session()
        response = session_obj.get(original_url, headers={"User-Agent": "Mozilla/5.0"})

        html = request.urlopen(request_site).read()
        raw = BeautifulSoup(html).get_text()
        # results = response.xpath('//body').get()
        # results = nltk.clean_html(str(results))
        item['NAICS_Code'] = self.ObjectDict[index]['NAICS_Code']
        item['Company_Name'] = self.ObjectDict[index]['Company_Name']
        item['URL'] = original_url
        item['Raw_Text'] = raw

        yield item
