import scrapy
from ..items import NaicsScraperItem
import re


def checkLen(info_list):
    if len(info_list) != 0:
        if len(info_list) == 2:
            return info_list[0], info_list[1]
        else:
            return info_list[0], ""
    else:
        return "", ""


class NAICS_Spider(scrapy.Spider):
    name = "companies"
    allowed_domains = ['']

    def __init__(self, *args, **kwargs):
        super(NAICS_Spider, self).__init__(*args, **kwargs)
        self.counter = 0
        self.start_urls = []
        # self.start_urls = ["https://www.naics.com/company-profile-page/?co=11028"]
        url = "https://www.naics.com/company-profile-page/?co="
        for i in range(1, 18500):
            self.start_urls.append(url + str(i))


    def parse(self, response):
        original_url = response.request.url
        NAICS_Code = re.search("=[0-9]+", original_url).group(0)
        print(NAICS_Code)
        NAICS_Code = NAICS_Code[1:]

        info_table = response.xpath('//table[@class="companyDetail topCompanyDetail"]/tr').getall()
        DUNS = response.xpath('//table[@class="companyDetail topCompanyDetail"]/tr[1]/td/strong/text()').getall()
        DUNS_status = response.xpath('//table[@class="companyDetail topCompanyDetail"]/tr[1]/td/strong/span/text()').get(default="")
        DUNS_num = DUNS[0].split()[1]

        # l2
        l2 = response.xpath('//table[@class="companyDetail topCompanyDetail"]/tr[2]/td/text()').getall()
        Company_Name, Tradestyle = checkLen(l2)

        # l3
        l3 = response.xpath('//table[@class="companyDetail topCompanyDetail"]/tr[3]/td/text()').getall()
        Top_Contact, Title = checkLen(l3) 

        Street_Address = response.xpath('//table[@class="companyDetail topCompanyDetail"]/tr[4]/td/text()').get(default="")
        Phone = response.xpath('//table[@class="companyDetail topCompanyDetail"]/tr[5]/td/text()').get(default="")
        URL = ""
        i = 0
        url_l6 = response.xpath('//table[@class="companyDetail topCompanyDetail"]/tr[6]/td/a/text()').getall()
        if len(url_l6) != 0:
            URL = url_l6[0]
            i = 1

        # l6 + i
        l6 = response.xpath('//table[@class="companyDetail topCompanyDetail"]/tr[' + str(6 + i) + ']/td/text()').getall()
        Total_Emps, Emps_On_Site = checkLen(l6)

        Sales_Volume = response.xpath('//table[@class="companyDetail topCompanyDetail"]/tr[' + str(7 + i) + ']/td/text()').get(default="")

        # l8
        l8 = response.xpath('//table[@class="companyDetail topCompanyDetail"]/tr[' + str(8 + i) + ']/td/text()').getall()
        Public_Private, Year_Started = checkLen(l8)

        # l9
        l9 = response.xpath('//table[@class="companyDetail topCompanyDetail"]/tr[' + str(9 + i) + ']/td/text()').getall()
        Lat, Long = checkLen(l9)

        # l10
        l10 = response.xpath('//table[@class="companyDetail topCompanyDetail"]/tr[' + str(10 + i) + ']/td/a/text()').getall()
        NAICS_1_num, NAICS_1_title = checkLen(l10)

        # l11
        l11 = response.xpath('//table[@class="companyDetail topCompanyDetail"]/tr[' + str(11 + i) + ']/td/a/text()').getall()
        NAICS_2_num, NAICS_2_title = checkLen(l11)

        # l12
        l12 = response.xpath('//table[@class="companyDetail topCompanyDetail"]/tr[' + str(12 + i) + ']/td/a/text()').getall()
        SIC_1_num, SIC_1_title = checkLen(l12)

        # l13
        l13 = response.xpath('//table[@class="companyDetail topCompanyDetail"]/tr[' + str(13 + i) + ']/td/a/text()').getall()
        SIC_2_num, SIC_2_title = checkLen(l13)

        Number_of_Family_Members = response.xpath(
            '//table[@class="companyDetail topCompanyDetail"]/tr[14]/td/text()').get(default="")
        Date_of_Report = response.xpath(
            '//table[@class="companyDetail topCompanyDetail"]/tr[15]/td/text()').get(default="")

        item = NaicsScraperItem()

        item['NAICS_Code'] = NAICS_Code
        item['DUNS_num'] = DUNS_num
        item['DUNS_status'] = DUNS_status
        item['Company_Name'] = Company_Name
        item['Tradestyle'] = Tradestyle
        item['Top_Contact'] = Top_Contact
        item['Title'] = Title
        item['Street_Address'] = Street_Address
        item['Phone'] = Phone
        item['URL'] = URL
        item['Total_Emps'] = Total_Emps
        item['Emps_On_Site'] = Emps_On_Site
        item['Sales_Volume'] = Sales_Volume
        item['Public_Private'] = Public_Private
        item['Year_Started'] = Year_Started
        item['Lat'] = Lat
        item['Long'] = Long
        item['NAICS_1_num'] = NAICS_1_num
        item['NAICS_1_title'] = NAICS_1_title
        item['NAICS_2_num'] = NAICS_2_num
        item['NAICS_2_title'] = NAICS_2_title
        item['SIC_1_num'] = SIC_1_num
        item['SIC_1_title'] = SIC_1_title
        item['SIC_2_num'] = SIC_2_num
        item['SIC_2_title'] = SIC_2_title
        item['Number_of_Family_Members'] = Number_of_Family_Members
        item['Date_of_Report'] = Date_of_Report

        yield item