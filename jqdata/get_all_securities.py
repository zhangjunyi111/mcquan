import pandas
from jqdatasdk import *

if __name__ == '__main__':
    auth('13366248789', 'HONGhong1225')
    # 获得2020年10月10日还在上市的所有股票列表
    df = get_all_securities(types=['index', 'fund', 'futures', 'etf', 'lof', 'fja', 'fjb', 'open_fund', 'bond_fund', 'stock_fund', 'QDII_fund', 'money_market_fund', 'mixture_fund', 'options', 'conbond'],
                            date='2023-09-10')
    mccode = list(df.index)
    print(df)
    df.insert(len(df.columns), column='mccode', value=mccode)
    df.to_excel('base_seurity_info4.xlsx', sheet_name='base_seurity_info.xlsx',
                index=False, )