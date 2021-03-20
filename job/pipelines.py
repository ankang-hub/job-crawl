# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql


class JobPipeline:
    def open_spider(self, spider):
        # 连接数据库
        self.connect = pymysql.connect(
            host='localhost',
            port=3306,
            db='information',
            user='root',
            passwd='617520',
            charset='utf8',
            use_unicode=True)
        # 通过cursor执行增删查改
        self.cursor = self.connect.cursor()
        self.connect.autocommit(True)

    def process_item(self, item, spider):
        # collection.insert(dict(item))
        sql = "insert into "+item['city_table']+" values('%s','%s','%s','%s')" \
              % (
                  item['title'],
                  item['price'],
                  item['requie'],
                  item['company'],

              )
        self.cursor.execute(sql)
        return item

    def close_spider(self, spider):
        self.cursor.close()
        self.connect.close()