# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NaicsScraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    NAICS_Code = scrapy.Field()
    DUNS_num = scrapy.Field()
    DUNS_status = scrapy.Field()
    Company_Name = scrapy.Field()
    Tradestyle = scrapy.Field()
    Top_Contact = scrapy.Field()
    Title = scrapy.Field()
    Street_Address = scrapy.Field()
    Phone = scrapy.Field()
    URL = scrapy.Field()
    Total_Emps = scrapy.Field()
    Emps_On_Site = scrapy.Field()
    Sales_Volume = scrapy.Field()
    Public_Private = scrapy.Field()
    Year_Started = scrapy.Field()
    Lat = scrapy.Field()
    Long = scrapy.Field()
    NAICS_1_num = scrapy.Field()
    NAICS_1_title = scrapy.Field()
    NAICS_2_num = scrapy.Field()
    NAICS_2_title = scrapy.Field()
    SIC_1_num = scrapy.Field()
    SIC_1_title = scrapy.Field()
    SIC_2_num = scrapy.Field()
    SIC_2_title = scrapy.Field()
    Number_of_Family_Members = scrapy.Field()
    Date_of_Report = scrapy.Field()



    pass


# class NaicsWebsiteItems(scrapy.Item):

