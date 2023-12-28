import re
import pandas as pd
with open('result20231110.txt') as f:
    result = f.read()
from datetime import datetime


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

# 修改时间格式为年-月-日
now = now.strftime("%Y-%m-%d")


data = {'mc_code': daimas, 'trade_date': now, 'open': jinkais, 'high':
    zuigaos, 'low': zuidis, 'pre_close':
            zuoshous, 'change': zhangdiees, 'pct_chg': zhangdiefus,
        'vol': chengjiaoliangs, 'amount': chengjiaoes, 'close':
            zuixinjias,
        'liangbi': liangbis, "huanshou": huanshoulvs,
        'mc_name': names,
        'zhenfu': zhenfus,
        'shiying': shiyinglvs, }
df = pd.DataFrame(data)
df.to_excel('20231110.xlsx')

df