# 获取2020-05-07当天证监会行业行业列表
import pandas
from jqdatasdk import *
from pandas import DataFrame

if __name__ == '__main__':
    auth('18435205109', '407504@Jun.')
    industries = ["sw_l1", "sw_l2", "sw_l3", "jq_l1", "jq_l2", "zjw"]
    df = pandas.DataFrame()
    for name in industries:
        df_new = get_industries(name=name, date='2022-08-11')
        length = df_new.shape[0]
        industry_type = length * [name]
    #     # print(industry_type)
        df_new.insert(len(df_new.columns), column='industry_type', value=industry_type)
        print('---------------------------df_new-------------------',df_new)
        df = df._append(df_new)
    industry_codes = list(df.index)
    df.reset_index(inplace=True)
    df = df.rename(columns={'index': 'industry_code'})
    print('-----------------------------df'
          '---------------------------------------\n', df)
    df2: DataFrame = pandas.DataFrame()
    for industry_code in industry_codes:
        stocks = get_industry_stocks(industry_code, date='2022-08-11')
        length = len(stocks)

        industry_codes2 = length * [industry_code]
        # print('-------------industry_codes2---------------\n', industry_codes2)
        industry_name = length * [df.loc[df['industry_code'] ==
                                         industry_code].iloc[0, 1]]
        industry_type = length * [df.loc[df['industry_code'] ==
                                         industry_code].iloc[0, 3]]
        # df3 = df.loc[df['industry_code'] == industry_code]
        # print('----------------df3--------------', df3)
        # industry_name = df.iloc[:]
        # print(df3.iloc[0,1])
        # print(df.loc[df['industry_code'] == industry_code])

        # print('-------------industry_name---------------\n', df)
        dict1 = {'industry_code': industry_codes2, "stock_code": stocks,
                 'industry_name': industry_name,'industry_type': industry_type}
        # print(industry_name)

        df2_new = pandas.DataFrame(dict1)
        # print(df2_new)
        df2 = pandas.concat([df2, df2_new])
    length = df2.shape[0]
    base_date = length * ['2022-06-24']
    df2.insert(len(df2.columns), column='trade_date', value = base_date)
    df2.to_excel('result.xlsx')
    print(df2)