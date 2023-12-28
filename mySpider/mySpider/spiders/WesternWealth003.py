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
        # now = '20230922'
        now = datetime.now()
        # 开启后爬前一天的数据，关闭后爬当天的数据
        # now = (now + timedelta(days=-2))
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
        lbcs = re.findall('"lbc":(.*?),', result)
        zbcs = re.findall('"zbc":(.*?),', result)
        days = re.findall('"days":(.*?),', result)
        cts = re.findall('"ct":(.*?)}', result)
        ztjjs = list(zip(days, cts))
        # logging.info("ztjjs的值为%s",ztjjs)
        new_ztjjs = []
        for ztjj in ztjjs:
            # for x, y in ztjj:
            # logging.info("ztjj的值为%s",ztjj)
            new_ztjjs.append(f'{ztjj[0]}/{ztjj[1]}')
        # logging.info("new_ztjjs的值为%s", new_ztjjs)

        length = len(daimas)
        trade_date = response.meta['date']
        # logging.warning('trade_date: %s', trade_date)
        trade_date = datetime.strptime(trade_date, "%Y%m%d")
        # logging.warning('trade_date: %s', trade_date)
        trade_date = datetime.date(trade_date)
        logging.info("trade_date 的type为,%s", type(trade_date))
        logging.info('trade_date: %s', trade_date)
        trade_dates = length * [trade_date]
        data = {
            'mc_code': daimas, 'mc_name': names, 'newest_price': zuixinjias,
            'amount': chengjiaoes,
            "huanshou": huanshoulvs, 'traded_market_value': liutongshizhis,
            'total_value':
                zongshizhis, 'industry':
                hybks, 'first_sealing_time': fbts, 'last_sealing_time': lbts,
            'trade_date': trade_dates, 'lbc': lbcs, 'zbc': zbcs, 'zttj':
                new_ztjjs}

        df = pd.DataFrame(data)
        # print(df)
        # df.to_excel(f'{trade_date}.xlsx')
        item = MyspiderItem()
        item["df"] = df
        yield item
