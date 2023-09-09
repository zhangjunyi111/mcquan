import scrapy
from urllib.parse import urlencode
import time
import random
import pandas as pd
import os
from ..items import MyspiderItem
import re
import logging
from datetime import datetime
from datetime import timedelta
global n


class ExampleSpider(scrapy.Spider):
    name = "WesternWealth"
    allowed_domains = ["http://quote.eastmoney.com/"]
    start_urls = 'https://push2ex.eastmoney.com/getTopicZTPool?cb' \
                 '=callbackdata9266123&ut=7eea3edcaed734bea9cbfc24409ed989' \
                 '&dpt=wz.ztzt&Pageindex=0&pagesize=500&sort=fbt%3Aasc&date' \
                 '={}&_=1692538530206'

    def start_requests(self):
        now = datetime.now()
        # 开启后爬前一天的数据，关闭后爬当天的数据
        now = (now + timedelta(days=-1))
        now = now.strftime("%Y%m%d")
        # # start_date = one_day_ago
        start_date = now
        trade_dates = pd.date_range(start=start_date, periods=1).strftime(
            "%Y%m%d").tolist()
        logging.info('trade_dates %s', trade_dates)
        for date in trade_dates:
            time.sleep(random.random())
            url = self.start_urls.format(date)
            yield scrapy.Request(
                url=url,
                meta={'date': date},
                callback=self.parse
            )

    def parse(self, response):
        writer = pd.ExcelWriter('20230909.xlsx')
        result = response.text
        daimas = re.findall('"c":"(.*?)",', result)
        names = re.findall('"n":"(.*?)"', result)
        zuixinjias = re.findall('"p":(.*?),', result)
        chengjiaoes = re.findall('"amount":(.*?),', result)
        liutongshizhis = re.findall('"ltsz":(.*?),', result)
        zongshizhis = re.findall('"tshare":(.*?),', result)
        hybks = re.findall('"hybk":"(.*?)",', result)
        fbts = re.findall('"fbt":(.*?),', result)
        lbts = re.findall('"lbt":(.*?),', result)
        huanshoulvs = re.findall('"hs":(.*?),', result)
        length = len(daimas)
        trade_date = response.meta['date']
        trade_dates = length * [response.meta['date']]
        data = {
            '股票代码': daimas, '公司名称': names, '最新价': zuixinjias, '成交': chengjiaoes,
            "换手": huanshoulvs, '流通市值': liutongshizhis, '总市值':
                zongshizhis, '所属行业':
                hybks, '首次封板时间': fbts, '最后封板时间': lbts, '交易日期': trade_dates}
        df = pd.DataFrame(data)
        # df.to_excel(f'{trade_date}.xlsx')
        item = MyspiderItem()
        item["df"] = df
        yield item

