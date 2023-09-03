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



class ExampleSpider(scrapy.Spider):
    name = "WesternWealth"
    allowed_domains = ["http://quote.eastmoney.com/"]
    start_urls = 'https://push2ex.eastmoney.com/getTopicZTPool?cb' \
                 '=callbackdata9266123&ut=7eea3edcaed734bea9cbfc24409ed989' \
                 '&dpt=wz.ztzt&Pageindex=0&pagesize=500&sort=fbt%3Aasc&date' \
                 '={}&_=1692538530206'

    def start_requests(self):
        now = datetime.now()
        one_day_ago = (now + timedelta(days=-1))
        one_day_ago = one_day_ago.strftime("%Y%m%d")
        start_date = one_day_ago
        trade_dates = pd.date_range(start=start_date, periods=1).strftime(
            "%Y%m%d").tolist()
        for date in trade_dates:
            time.sleep(random.random())
            url = self.start_urls.format(date)
            yield scrapy.Request(
                url=url,
                meta={'date': date},
                callback=self.parse
            )

    def parse(self, response):

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
        trade_date = length * [response.meta['date']]
        data = {
            '股票代码': daimas, '公司名称': names, '最新价': zuixinjias, '成交': chengjiaoes,
            "换手": huanshoulvs, '流通市值': liutongshizhis, '总市值':
                zongshizhis, '所属行业':
                hybks, '首次封板时间': fbts, '最后封板时间': lbts, '交易日期': trade_date}
        df = pd.DataFrame(data)
        item = MyspiderItem()
        item["df"] = df

        # logging.info('daimas的值为{}'.format(daimas))
        # logging.info('df的值为{}'.format(df))
        # logging.info('trade_date的值为{}'.format(trade_date))
        yield item

