import json
import re
import pandas as pd
# with open('./result6.txt', 'r', encoding="utf-8") as f:
#     data = json.load(f)
# print(data.keys())
# print((data['data'].keys()))

# with open('./data3.txt', 'w', encoding="utf-8") as f:
#     json.dump(data["data"], f, ensure_ascii=False, indent=4)
with open('result9.txt', 'r', encoding="utf-8") as f:
    result = f.read()
# print(result)

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
print(len(daimas))
print(len(names))
data = {'股票代码': daimas, '公司名称': names, '最新价': zuixinjias, '涨跌幅': zhangdiefus, '涨跌': zhangdiees,
        '成交量': chengjiaoliangs, '成交': chengjiaoes, '振幅': zhenfus,
        '最高价': zuigaos, '最低价': zuidis, '今开': jinkais, '昨收': zuoshous, '量比': liangbis, "换手": huanshoulvs,
        '实盈':shiyinglvs}
df = pd.DataFrame(data)
print(df)
df.to_excel('股票_20230813.xlsx', sheet_name='sheet1', index=False)