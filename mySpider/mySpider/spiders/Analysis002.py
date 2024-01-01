# -*- coding: utf-8 -*-
import json
import re
import pandas as pd
import os

path = '/涨停板'
files = os.listdir(path)


def parse(path,files):
    os.chdir(path)
    df = pd.DataFrame()
    for file in files:
        try:
            with open(file, 'r', encoding="utf-8") as f:
                result = f.read()
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
                trade_date = re.findall(r'\d+', file)[0]
                trade_date = length*[trade_date]
                data = {
                    '股票代码': daimas, '公司名称': names, '最新价': zuixinjias, '成交': chengjiaoes,
                       "换手": huanshoulvs, '流通市值': liutongshizhis, '总市值':
                            zongshizhis, '所属行业':
                hybks, '首次封板时间': fbts, '最后封板时间': lbts, '交易日期': trade_date}

                if df.empty:
                    df = pd.DataFrame(data)
                else:
                    new = pd.DataFrame(data)
                    df = df._append(new, ignore_index=True)
                    print(df.shape[0])
        except Exception as e:
            print(e)
            continue
    print(df.shape[0])
    df.to_excel('result.xlsx', sheet_name='sheet1', index=False)

parse(path,files)