import scrapy
from urllib.parse import urlencode
import time
import random
import pandas as pd
import os
from Analysis002 import parse


class ExampleSpider(scrapy.Spider):
    name = "WesternWealth"
    allowed_domains = ["http://quote.eastmoney.com/"]
    start_urls = 'https://push2ex.eastmoney.com/getTopicZTPool?cb' \
                 '=callbackdata9266123&ut=7eea3edcaed734bea9cbfc24409ed989' \
                 '&dpt=wz.ztzt&Pageindex=0&pagesize=500&sort=fbt%3Aasc&date' \
                 '={}&_=1692538530206'

    def start_requests(self):
        start_date = '20230801'
        trade_dates = pd.date_range(start=start_date, periods=20).strftime(
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
        current_dir = os.getcwd()
        if 'result_files' not in current_dir:
            result_files = os.path.join(current_dir, 'result_files')
            os.mkdir(result_files)
            os.chdir(result_files)
        with open('result-{}.txt'.format(response.meta['date']), 'w',
                  encoding="utf-8") as f:
            f.write(result)

