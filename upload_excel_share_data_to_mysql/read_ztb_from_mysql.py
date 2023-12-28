import logging

from mysqldb import MysqlDb
import pandas as pd
from mysqldb import CreateLogger
import os

logging.basicConfig(level=logging.NOTSET)
mysql = MysqlDb()
my_logger = CreateLogger()
mylogger = my_logger.create_logger()
engine = mysql.connect_mysql(mylogger)


def read_ztb_from_mysql():
    # 创建数据库引擎
    engine = mysql.connect_mysql(mylogger)
    # 从数据库读取涨停板
    mc_code = mysql.read_ztb(engine, mylogger)
    mc_code.to_excel('mc_code.xlsx')


read_ztb_from_mysql()


