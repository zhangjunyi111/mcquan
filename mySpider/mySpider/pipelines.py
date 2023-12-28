"""
Date:20230903
Auther:zhangjunyi
Email:18435205109@163.com
"""
# Define your item pipelines here
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# useful for handling different item types with a single interface

import logging
import typing
import sys
from datetime import datetime

import pandas as pd

from .mysqldb import MysqlDb

# logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, filename='westernWealth.log',
                    filemode='w')


def set_pandas_display_options() -> None:
    display = pd.options.display
    display.max_columns = 100000000000000000
    display.max_rows = 10000000000000000
    display.max_colwidth = 199
    display.width = None


set_pandas_display_options()


class MyspiderPipeline:
    def __init__(self, mysql_url):
        """
        :param mysql_url: mysqlurl连接到数据库
        """
        self.mysql_url = mysql_url
        self.session = None
        self.mysql_table1 = 'uplimit_stock'
        self.mysql_table2 = 'dict_table'
        # self.logger = logger

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mysql_url=crawler.settings.get("MYSQL_URL"),
        )

    def open_spider(self, spider):
        """

        :param spider:
        :return:
        """
        self.session = MysqlDb()
        self.session.mysql_eng = self.session.connect_mysql(self.mysql_url)

    def process_item(self, item, spider):
        """
        :param item:
        :param spider:
        :return:
        """

        df = item["df"]
        print("********************")
        self.session.write_to_mysql(df, 'append', self.session.mysql_eng,
                                    self.mysql_table1,
                                    )
        ts_codes = df['mc_code'].tolist()
        company_names = df['mc_name'].tolist()
        trade_dates = df['trade_date'].tolist()
        print(trade_dates)
        datas = list(zip(ts_codes, company_names, trade_dates))
        df_dict_table = pd.read_sql_table(self.mysql_table2,
                                          self.session.mysql_eng)
        for data in datas:
            if data[0] in df_dict_table['ts_code'].tolist():
                logging.info('if分支')
                # 更新涨停次数
                df_dict_table.loc[(df_dict_table[
                                       'ts_code'] == data[
                                       0]), 'limit_increases_number'] = \
                    df_dict_table.loc[(df_dict_table[
                                           'ts_code'] == data[
                                           0]), 'limit_increases_number'] + 1
                # 更新涨停时间
                df_dict_table.loc[(df_dict_table[
                                       'ts_code'] == data[0]), 'end_time'] = \
                    data[2]

            else:
                logging.info('else分支')
                new_dict = {'ts_code': data[0], 'company_name': data[1],
                            'start_time': data[2],
                            'limit_increases_number': 1}
                new_df = pd.DataFrame(new_dict, index=[0])
                df_dict_table = pd.concat([new_df, df_dict_table])

        try:
            trade_date = df['交易日期'].tolist()[0]
            df_dict_table.to_excel(f'{trade_date}.xlsx')
        except Exception as e:
            print(e)
        # logging.info('dict_table %s', df_dict_table)
        self.session.write_to_mysql(df_dict_table, 'replace',
                                    self.session.mysql_eng, self.
                                    mysql_table2,
                                    )
        # print("Exiting the program...")
        # sys.exit(0)
        return df_dict_table

    def close_spider(self, spider):
        """
        :param spider:
        :return:
        """
        self.session.close_connect()
        return


# class MyspiderPipeline2:
#     """
#     :param mysql_url: mysqlurl连接到数据库
#     """
#     def __init__(self, mysql_url):
#         self.mysql_url = mysql_url
#         self.session = None
#         self.mysql_table1 = 'uplimit_stock'
#         self.mysql_table2 = 'dict_table'
#
#     @classmethod
#     def from_crawler(cls, crawler):
#         return cls(
#             mysql_url=crawler.settings.get("MYSQL_URL"),
#         )
#
#     def open_spider(self, spider):
#         """
#         :param spider:
#         :return:
#         """
#         self.session = MysqlDb()
#         self.session.mysql_eng = self.session.connect_mysql(self.mysql_url)
#
#     def process_item(self, df_dict_table, spider):
#         print(df_dict_table)
#         return
#
#
#
#     def close_spider(self, spider):
#         """
#         :param spider:
#         :return:
#         """
#         self.session.close_connect()
#         return
#
