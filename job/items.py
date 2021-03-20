# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JobItem(scrapy.Item):
    # 每张表 保存招聘相关信息信息
    city_table = scrapy.Field() # 窜表的表名
    title = scrapy.Field()
    price = scrapy.Field()
    requie = scrapy.Field()
    company =scrapy.Field()
    print('\n',title,'\n',price,'\n',requie,'\n',company)
    print('------------------------------------------------')