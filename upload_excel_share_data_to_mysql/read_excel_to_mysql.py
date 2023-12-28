import logging

from mysqldb import MysqlDb
import pandas as pd
from mysqldb import CreateLogger
import os

logging.basicConfig(level=logging.NOTSET)
path = r'F:\分时数据下载\2023年'
count = 0
mysql = MysqlDb()

my_logger = CreateLogger()
mylogger = my_logger.create_logger()
engine = mysql.connect_mysql(mylogger)
paths = []

mc_codes = pd.read_excel('mc_code.xlsx', converters={u'mc_code': str})[
    'mc_code'].tolist()
logging.info('mc_codes:%s', mc_codes)
mc_codes_with_name = []
for mc_code in mc_codes:
    if mc_code.startswith('0') or mc_code.startswith('3'):
        mc_code = 'SZ.' + mc_code
        mc_codes_with_name.append(mc_code)
    elif mc_code.startswith('6'):
        mc_code = 'SH.' + mc_code
        mc_codes_with_name.append(mc_code)
logging.info(mc_codes_with_name)


for root, dir, file in os.walk(path):
    # print('根目录', root)
    # print('文件夹列表', dir)
    # print('文件列表', file)
    if file:
        for file_ in file:
            logging.info('file_name:%s', file_[:-4])
            if file_[:-4] in mc_codes_with_name:
                file__ = os.path.join(root, file_)
                # print(f'file__:{file__}')
                paths.append(file__)
                # print(file__)
                # print(len(paths))
                # count += 1
                # df = pd.read_csv(file__)
                # mysql.to_mysql(df, engine, mylogger)
                # logging.info(f'{file_}中的数据已经被插入')

# df = pd.read_csv(r'F:\分时数据下载\2023年\2013年中\SH.601069.csv')
# print(df)
for file in paths:
    # print(file)
    # print(rf'{file}')
    df = pd.read_csv(rf'{file}', header=0, index_col=0)
    # df = pd.read_excel(rf'{file}')
    # print(df)
    mysql.to_mysql(df, engine, mylogger)
    count += 1
    print('----------------count-----------\n', count)
    # logging.info(f'{file_}中的数据已经被插入')
print(count)