import scrapy
from urllib.parse import urlencode
import time
import random


class ExampleSpider(scrapy.Spider):
    name = "WesternWealth"
    allowed_domains = ["http://quote.eastmoney.com/"]
    start_urls = 'http://28.push2.eastmoney.com/api/qt/clist/get?'

    def start_requests(self):
        for page in range(1, 2):
            time.sleep(random.random())
            params = (('cb', 'jQuery112407879169571877849_1691836618709'),
                  ("pn", str(page)),
                  ('pz', 20),
                  ("po", 1),
                  ('np', 1),
                  ('ut', "bd1d9ddb04089700cf9c27f6f7426281"),
                  ("fltt", 2),
                  ('invt', 2),
                  ('wbp2u', '|0|0|0|web'),
                  ('fid', 'f3'),
                  ('fs', 'm:0 t:6 m:0 t:80 m:1 t:2 m:1 t:23 m:0 t:81 s:2048'),
                  ("fields", 'f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152'),
                  ('_', 1691836619272))
            params = urlencode(params)
            url = self.start_urls + params
            print(url)
            yield scrapy.Request(
                url,
                callback=self.parse
            )

    def parse(self, response):
        # print()
        result = response.text
        # print(result)
        # pass
        with open('result9.txt', 'a+', encoding="utf-8") as f:
            f.write(result)

