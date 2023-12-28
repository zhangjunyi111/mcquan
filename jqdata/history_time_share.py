# import requests, re
# import execjs
#
#
# def get_last_5days_data(code: str):
#     '''获取指定股票最近5天的分时线数据(含当天)'''
#     url = 'https://finance.sina.com.cn/realstock/company/%s/hisdata/klc_cm.js' % (
#         code)  # 指定日期对应的最近5天的分时数据 KLC_ML_szxxxxxx=
#     prefix = 'KLC_ML_%s=' % code
#     res = requests.get(url)
#     if res.status_code == 200:
#         reg = re.compile(r'%s"(.+?)"' % prefix)
#         data = reg.findall(res.text)
#
#     with open('./sf_sdk.js', 'r') as f:
#         js_file = f.read()
#     ctx = execjs.compile(js_file)
#     days_data = data[0].split(',')
#     for i in range(len(days_data)):
#         arr = ctx.call('decode', days_data[i])
#         print(arr[0])
#
#
# def get_month_data(code: str, date: str):
#     '''获取日期所在月份的所有分时数据(如果是当前月，不含当天的)'''
#     year = date[0:4]
#     month = date[5:7]
#     url = 'http://finance.sina.com.cn/realstock/company/%s/hisdata/%s/%s.js?d=%s' % (
#     code, year, month, date)  # 指定日期所在月份的所有分时数据  MLC_szxxxxxx_2021_04=
#     prefix = 'MLC_%s_%s_%s=' % (code, year, month)
#     res = requests.get(url)
#     if res.status_code == 200:
#         reg = re.compile(r'%s"(.+?)"' % prefix)
#         data = reg.findall(res.text)
#
#     with open('./sf_sdk.js', 'r') as f:
#         js_file = f.read()
#     ctx = execjs.compile(js_file)
#     days_data = data[0].split(',')
#     for i in range(len(days_data)):
#         arr = ctx.call('decode', days_data[i])
#         print(arr[0])
#
#
# if __name__ == '__main__':
#     get_month_data('sz000001', '2021-11-07')
#     # get_last_5days_data('sz000001')
d = get_ticks("000001.XSHE",start_dt=None, end_dt="2018-07-03", count=8)
print(d)