# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
# from itemadapter import ItemAdapter
from pymongo import MongoClient



class NaicsScraperPipeline:
    # pass
    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def __init__(self, crawler):
        self.client = MongoClient('mongodb://localhost:27017')
        self.collection = 'NAICS_DB'
        self.db = self.client[self.collection]
        self.table_NAICS = self.db['db_test']
        self.new_data = 0
        self.crawler = crawler

    def process_item(self, item, spider):
        if self.table_NAICS.count_documents({'NAICS_Code': item["NAICS_Code"]}, limit=1) == 0:
            self.table_NAICS.insert_one(dict(item))
            self.new_data += 1
        # if self.new_data >= 500:
        #     self.crawler.engine.close_spider(spider, "got 500 new data")
        return item
