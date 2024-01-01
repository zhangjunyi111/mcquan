#! /usr/bin/python
# _*_ coding:utf-8 _*_

from sqlalchemy import create_engine
import pandas as pd
from datetime import datetime
import pymysql


def create_mysql_engine() -> any:
    # 利用pymysql创建数据库连接
    # db_conn = pymysql.connect(
    #     host='123.56.254.64',
    #     port=3306,
    #     user='root',
    #     password='HONGhong1225',
    #     database='mcquant',
    #     charset='utf8')
    db_conn = create_engine('mysql://root:HONGhong1225@123.56.254.64/mcquant')
    return db_conn

# def create_mysql2_engine():
#     db_conn = pymysql.connect(
#         host='47.119.175.107',
#         port=3306,
#         user='root',
#         password='HONGhong1225',
#         database='mcquant',
#         charset='utf8'
#     )


def read_dipei_write_gaopei() :
    """
    :return:涨停板的股票列表
    """
    new_codes = []
    start_date = '2023-01-03'
    end_date = '2023-12-29'
    date_range = pd.date_range(start_date, end_date)
    db_conn = create_engine('mysql+pymysql://root:HONGhong1225@123.56.254.64'
                            '/mcquant', echo=True)
    db_conn2 = create_engine(
        'mysql+pymysql://root:HONGhong1225@47.119.175.107/mcquant', echo=True)

    for date in date_range:
        date_str = str(date)
        date_str_ = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S').strftime(
            '%Y-%m-%d')
    # 读取服务器的涨停代码
        ztb_stock = pd.read_sql(
        f"select mc_code from ztb_stock where DATE_FORMAT(STR_TO_DATE("
        f"trade_date,"
        f"'%%Y-%%m-%%d %%H:%%i:%%s'),'%%Y-%%m-%%d') = '{date_str_}'", db_conn)
    # 读取字段表中的ts_code列
        if ztb_stock.empty:
            continue
        codes = ztb_stock[
        'mc_code'
        ]
    # 因为腾讯的分时数据的接口的格式参数code的格式为shx(上海的证券交易所平台),skewx为深圳交易所平台。
        for code in codes:
            if code.startswith('0'):
               code = code.replace('0', 'SZ.0', 1)
            elif code.startswith('3'):
                code = code.replace('3', 'SZ.3', 1)
            elif code.startswith('6'):
                code = code.replace('6', 'SH.6', 1)
            df = pd.read_sql(f"select * from fsdata_copy where "
                                 f"DATE_FORMAT(STR_TO_DATE(time, '%%Y-%%m-%%d "
                                 f"%%H:%%i:%%s'),'%%Y-%%m-%%d') = '"
                             f"{date_str_}' and mc_code"
                             f"='{code}'", db_conn2)
            # df.to_sql('fs_data', con=db_conn, if_exists='append')
            print(df)

read_dipei_write_gaopei()
