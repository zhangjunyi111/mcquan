# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import logging
from .mysqldb import MysqlDb
from .mysqldb import CreateLogger


class MyspiderPipeline:
    def open_spider(self):
        self.mylogger = CreateLogger()
        self.mylogger = self.mylogger.create_logger()

    def process_item(self, item, spider):

        df = item["df"]
        mysql = MysqlDb()
        engline = mysql.connect_mysql(self.mylogger)
        mysql.to_mysql(df, 'uplimit_stock', engline, self.mylogger)

        return item
