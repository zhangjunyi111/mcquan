import scrapy
import pandas as pd
import datetime
import pymysql
import typing
import requests
import json
from sqlalchemy import create_engine
import pymysql
pymysql.install_as_MySQLdb()


class GetTimeShareSpider(scrapy.Spider):
    name = "get_time_share"
    allowed_domains = ["web.ifzq.gtimg.cn"]
    start_urls = ["https://web.ifzq.gtimg.cn"]

    import pandas as pd
    import datetime
    import pymysql
    import typing
    import requests
    import json
    from sqlalchemy import create_engine
    import pymysql
    pymysql.install_as_MySQLdb()

    def create_mysql_engine(self) -> any:
        # 利用pymysql创建数据库连接
        # db_conn = pymysql.connect(
        #     host='123.56.254.64',
        #     port=3306,
        #     user='root',
        #     password='HONGhong1225',
        #     database='mcquant',
        #     charset='utf8')
        db_conn = create_engine(
            'mysql://root:HONGhong1225@123.56.254.64/mcquant')
        return db_conn

    def get_codes(self) -> list:
        """
        :return:涨停板的股票列表
        """
        new_codes = []
        db_conn = self.create_mysql_engine()
        # 读取服务器的字典表
        mc_code = pd.read_sql('select distinct mc_code from \
            base_daily_stock', db_conn)
        # 读取字段表中的ts_code列
        codes = mc_code['mc_code'].tolist()
        # 因为腾讯的分时数据的接口的格式参数code的格式为shxxxx(上海的证券交易所平台),szxxx为深圳交易所平台。
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
        return new_codes

    def get_result(self, new_codes: list):
        """
        :param new_codes: 传入涨停板的代码
        :return: 返回涨停板的分时数据，Dataframe格式
        """
        proxy = '45.9.8.34'
        # 格式化当前日期
        date = datetime.datetime.now().strftime('%Y-%m-%d')
        db_conn2 = self.create_mysql_engine()
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
                                  columns=['time', 'price', 'amount', 'vol',
                                           'mccode',
                                           'date'])
                # print(df)
                # 利用pandas的contat函数将旧的结果与新结果拼接起来。
                myresult = pd.concat([myresult, df])
                print(myresult.shape)
            except Exception as e:
                continue
        myresult.to_excel(f'{date}.xlsx')
        # myresult.to_sql(name='time_share', con=db_conn2,
        #                 if_exists='append',
        #                 index_label=False, index=False)
        return

    def start_requests(self):
        codes = self.get_codes()
        self.get_result(codes)
        print('分时数据爬虫程序运行结束')

    def parse(self, response):
        pass
