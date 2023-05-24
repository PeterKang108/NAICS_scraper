from pymongo import MongoClient
from bs4 import BeautifulSoup
import re

import urllib
from urllib import request
from urllib.request import Request, urlopen
import requests

client = MongoClient('mongodb://localhost:27017')
collection = 'NAICS_DB'
db = client[collection]
table_NAICS = db['db_test']
table_web = db['db_url']
results = table_NAICS.find({}, {'URL': 1, 'NAICS_Code': 1, 'Company_Name': 1, '_id': 0})
results = list(results)

db_dict = results

for data in db_dict:
    print(data["NAICS_Code"])
    exist = table_web.find({'NAICS_Code': data['NAICS_Code']})
    exist = list(exist)

    original_url = "https://" + data['URL']
    request_site = Request(original_url, headers={"User-Agent": "Mozilla/5.0"})

    try:
        html = request.urlopen(request_site, timeout=10).read()
    except:
        continue

    raw = BeautifulSoup(html, features="lxml").get_text()
    raw = raw.strip()
    raw = raw.replace("\n", " ")
    raw = raw.replace("\t", " ")
    raw = re.sub(" +", " ", raw)
    if len(exist) != 0:
        print(data["NAICS_Code"] + " updated")
        table_web.update_one({'NAICS_Code': data['NAICS_Code']},
                             {"$set": {'raw_text': raw}})
        continue
    table_web.insert_one(
        {'URL': data['URL'], 'NAICS_Code': data['NAICS_Code'], 'Company_Name': data['Company_Name'], 'raw_text': raw})
