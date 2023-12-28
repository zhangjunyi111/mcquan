import scrapy
from urllib.parse import urlencode
import time
import random
import re
import pandas as pd
import sqlalchemy

class ExampleSpider(scrapy.Spider):
    name = "WesternWealth"
    allowed_domains = ["http://quote.eastmoney.com/"]
    start_urls = 'http://48.push2.eastmoney.com/api/qt/clist/get?cb' \
                 '=jQuery112402508937289440778_1658838703304&pn={' \
                 '}&pz=20&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt' \
                 '=2&invt=2&wbp2u=|0|0|0|web&fid=f3&fs=m:0+t:6,m:0+t:80,' \
                 'm:1+t:2,m:1+t:23,m:0+t:81+s:2048&fields=f1,f2,f3,f4,f5,f6,' \
                 'f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,' \
                 'f25,f22,f11,f62,f128,f136,f115,f152&_=1658838703305 '

    def start_requests(self):
        for page in range(1, 276):
            time.sleep(random.random())
            url = self.start_urls.format(page)
            yield scrapy.Request(
                url,
                callback=self.parse
            )

    def parse(self, response):
        engine = sqlalchemy.create_engine(
            'mysql+pymysql://root:HONGhong1225@123.56.254.64'
            '/mcquant'
            '', echo=True)
        result = response.text
        daimas = re.findall('"f12":"(.*?)",', result)
        names = re.findall('"f14":"(.*?)"', result)
        zuixinjias = re.findall('"f2":(.*?),', result)
        zhangdiefus = re.findall('"f3":(.*?),', result)
        zhangdiees = re.findall('"f4":(.*?),', result)
        chengjiaoliangs = re.findall('"f5":(.*?),', result)
        chengjiaoes = re.findall('"f6":(.*?),', result)
        zhenfus = re.findall('"f7":(.*?),', result)
        zuigaos = re.findall('"f15":(.*?),', result)
        zuidis = re.findall('"f16":(.*?),', result)
        jinkais = re.findall('"f17":(.*?),', result)
        zuoshous = re.findall('"f18":(.*?),', result)
        liangbis = re.findall('"f10":(.*?),', result)
        huanshoulvs = re.findall('"f8":(.*?),', result)
        shiyinglvs = re.findall('"f9":(.*?),', result)
        data = {'股票代码': daimas, '公司名称': names, '最新价': zuixinjias,
                '涨跌幅': zhangdiefus, '涨跌': zhangdiees,
                '成交量': chengjiaoliangs, '成交': chengjiaoes, '振幅': zhenfus,
                '最高价': zuigaos, '最低价': zuidis, '今开': jinkais, '昨收': zuoshous,
                '量比': liangbis, "换手": huanshoulvs,
                '实盈': shiyinglvs}
        df = pd.DataFrame(data)
        df.to_sql('daily_stock', con=engine, if_exists="append", index=False)

