import pandas as pd
import datetime
import pymysql
import typing
import requests
import json
from sqlalchemy import create_engine
import pymysql
import datetime

pymysql.install_as_MySQLdb()
today = datetime.date.today()


def create_mysql_engine() -> any:
    # 利用pymysql创建数据库连接
    db_conn = pymysql.connect(
        host='123.56.254.64',
        port=3306,
        user='root',
        password='HONGhong1225',
        database='mcquant',
        charset='utf8')
    db_conn = create_engine('mysql://root:HONGhong1225@123.56.254.64/mcquant')
    return db_conn


def get_codes() -> list:
    """
    :return:涨停板的股票列表
    """
    new_codes = []
    db_conn = create_mysql_engine()
    # 读取服务器的字典表
    ztb_stock = pd.read_sql(f"select mc_code from ztb_stock where trade_date "
                            f"='2023-12-28'", db_conn)
    # 读取字段表中的ts_code列
    codes = ztb_stock[
        'mc_code'
    ]
    # 因为腾讯的分时数据的接口的格式参数code的格式为shx(上海的证券交易所平台),skewx为深圳交易所平台。
    for code in codes:
        if code.startswith('0'):
            code = code.replace('0', 'sz0', 1)
            new_codes.append(code)
        elif code.startswith('3'):
            code = code.replace('3', 'sz3', 1)
            new_codes.append(code)
        elif code.startswith('6'):
            code = code.replace('6', 'sh6', 1)
            new_codes.append(code)
    print('new_codes',new_codes)
    return new_codes


def get_result(new_codes: list):
    """
    :param new_codes: 传入涨停板的代码
    :return: 返回涨停板的分时数据，Dataframe格式
    """
    proxy = '45.9.8.34'

    # 格式化当前日期
    date = datetime.datetime.now().strftime('%Y-%m-%d')
    db_conn2 = create_mysql_engine()
    headers = {'content-type': 'application/json', "proxy": proxy}

    # 创建空的Dataframe准备接收返回的数据
    myresult = pd.DataFrame()
    for code in new_codes:
        try:
            datas = []
            url = f'https://web.ifzq.gtimg.cn/appstock/app/minute/query?code={code}'
            res = requests.post(url=url, headers=headers, )
            simWords = res.json()
            # 根据simWords的格式进行解析
            simWords = simWords['data'][code]['data']['data']
            for data in simWords:
                data = data.split(' ')
                data.append(code)
                data.append(date)
                datas.append(data)
            df = pd.DataFrame(datas,
                              columns=['time', 'price', 'amount', 'vol', 'mccode',
                                       'date'])
            print(df)
        except Exception as e:
            continue

        # 利用pandas的contact函数将旧的结果与新结果拼接起来。
        myresult = pd.concat([myresult, df])
    myresult.to_sql(name='fs_data', con=db_conn2,
                          if_exists='append',
                          index_label=False, index=False)
    return


if __name__ == '__main__':
    codes = get_codes()
    get_result(codes)
