from openpyxl import load_workbook
import pandas as pd
import os
import requests
import json
# code = 'sh600006'
# df = pd.read_excel(f'sh600031.xlsx')
# print(df)
#
# if os.path.exists(f'{code}.xlsx'):
#     df_old = pd.read_excel(f'{code}.xlsx')
#     df = pd.concat([df, df_old])
#     df.to_excel(f'{code}.xlsx')
# else:
#     # pd.to_excel(f'{code}.xlsx'
#     #             )
#     df.to_excel(f'{code}.xlsx')

res = requests.post('https://web.ifzq.gtimg.cn/appstock/app/minute/query?code'
                    '=sh603232')
print(type(res.json()))
print(res.json())
with open('res.json', 'w') as f:
    json.dump(res.json(), f, ensure_ascii=False, indent=4)