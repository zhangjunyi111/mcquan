"""
Date:20230903
Auther:zhangjunyi
Email:18435205109@163.com
"""
import sqlalchemy
import pandas as pd
import logging
logger = logging.getLogger(__name__)

class MysqlDb(object):

    def __init__(self):
        self.logger = logger
        self.engine = None

    def connect_mysql(self, mysql_url):
        """
        :return: 返回数据库连接
        """
        self.engine = sqlalchemy.create_engine(
            mysql_url, echo=True)
        logging.info('创建数据库引擎成功!')
        return self.engine

    def write_to_mysql(self, df,if_exists, engine, table_name):
        """
        :param df: Dataframe对象
        :param table_name: Mysql数据库表名
        :return:
        """
        if if_exists == 'append':
            df.to_sql(table_name, con=engine
                      , if_exists='append', index=False)
        if if_exists == 'replace':
            df.to_sql(table_name, con=engine
                  , if_exists='replace', index=False)

        self.logger.info('插入数据库成功!')
        return ''

    # def read_mysql(self, df, engine, table_name):
    #     sql = 'select ts_code from {}'.format(table_name)
    #     ts_codes = df.read_sql(con=engine, sql=sql)
    #     return ts_codes


    def close_connect(self):
        """
        :return:
        """
        self.engine.dispose()
        self.logger.info("关闭数据库引擎!")
        return ''





