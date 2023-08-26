import pandas as pd
import sqlalchemy
import os
pd.set_option('display.max_columns', None)
engine = sqlalchemy.create_engine(
    'mysql+pymysql://root:HONGhong1225@123.56.254.64'
    '/mcquant'
    '', echo=True)


# 按股票代码查询，支持多个股票代码输入
# 按日期查询，起止日期和终止日期
def daily(ts_code, begin_date, end_date, fields):
    fields = ','.join(fields)
    print(fields)
    sql = 'select {} from Shanghai_Shenzhen_Beijing_A_stocks  where ts_code ' \
          'in {} AND trade_date >= "{}" AND trade_date <= "{}"'.format(
        fields, ts_code, begin_date, end_date)
    res = pd.read_sql(sql, engine)
    return res


# 将excel表存储到mysql数据库
def save_to_mysql_database():
    files = os.listdir('./2021年')
    for file in files:
        print(file)
        try:
            # 循环读取excel文件
            df = pd.read_excel('./2021年/{}'.format(file))
            del df['Unnamed: 0']
            df.to_sql('daily_stock', con=engine, if_exists="append", index=False)
        except Exception as e:
            print(e)
        continue


if __name__ == '__main__':
    # 调用接口查询daily数据
    # result = daily('(300630,002459)', '2023-08-13', '2023-08-13', ['ts_code',
    # 'open'

    # 调用接口将excel写入到数据库
    save_to_mysql_database()

