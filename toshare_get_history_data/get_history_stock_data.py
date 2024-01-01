import tushare as ts
import pandas as pd

ts.set_token('30226611db36a579489d1700d29d2e04149b31d0dbfa203e6c7d9338')
start_date = '20210101'
pro = ts.pro_api()
trade_dates = pd.date_range(start=start_date, periods=365).strftime(
    "%Y%m%d").tolist()

for trade_date in trade_dates:
    df = pro.daily(trade_date=trade_date)
    print(df)
    print('--------{}--------'.format(trade_date))
    df.to_excel('result{}.xlsx'.format(trade_date), sheet_name=str(trade_date))

