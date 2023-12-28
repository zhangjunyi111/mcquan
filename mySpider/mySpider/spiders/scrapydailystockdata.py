import scrapy
from urllib.parse import urlencode
import time
import random
import re
import pandas as pd
import sqlalchemy
import logging
from datetime import datetime


class ScrapydailystockdataSpider(scrapy.Spider):
    name = "scrapydailystockdata"
    allowed_domains = ["http://quote.eastmoney.com/"]
    start_urls = 'http://48.push2.eastmoney.com/api/qt/clist/get?cb' \
                 '=jQuery112402508937289440778_1658838703304&pn={' \
                 '}&pz=20&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt' \
                 '=2&invt=2&wbp2u=|0|0|0|web&fid=f3&fs=m:0+t:6,m:0+t:80,' \
                 'm:1+t:2,m:1+t:23,m:0+t:81+s:2048&fields=f1,f2,f3,f4,f5,f6,' \
                 'f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,' \
                 'f25,f22,f11,f62,f128,f136,f115,f152&_=1658838703305 '

    def start_requests(self):
        for page in range(1, 4):
            time.sleep(random.random())
            url = self.start_urls.format(page)
            yield scrapy.Request(
                url,meta={'page':page},
                callback=self.parse
            )

    def parse(self, response):
        engine = sqlalchemy.create_engine(
            'mysql+pymysql://root:HONGhong1225@47.93.89.155'
            '/mcquant'
            '', echo=True)
        result = response.text
        with open('result20231110.txt', 'a') as f:
            f.write(result)
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
        now = datetime.now()
        # # 修改时间格式为年-月-日
        # now = now.strftime("%Y-%m-%d")
        # logging.info('now的值为: %s', now)
        data = {'mc_code': daimas, 'trade_date': now, 'open': jinkais, 'high':
            zuigaos, 'low': zuidis, 'pre_close':
                    zuoshous, 'change': zhangdiees, 'pct_chg': zhangdiefus,
                'vol': chengjiaoliangs, 'amount': chengjiaoes, 'close':
                    zuixinjias,
                'liangbi': liangbis, "huanshou": huanshoulvs,
                'mc_name': names,
                'zhenfu': zhenfus,
                'shiying': shiyinglvs, }
        page = response.meta['page']
        df = pd.DataFrame(data)
        logging.info('df的值为 %s', df)
        df.to_sql('Sheet', con=engine, if_exists="append", index=False)
        df.to_excel(f'20231117_{page}.xlsx')
