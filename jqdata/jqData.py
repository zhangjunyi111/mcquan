import pandas
from jqdatasdk import *

if __name__ == '__main__':
    auth('13366248789', 'HONGhong1225')

    # 查询当日剩余可调用数据条数
    # count=get_query_count()
    # print(count)









    # 获取2020-05-07当天证监会行业行业列表
    industries = ["sw_l1", "sw_l2", "sw_l3", "jq_l1", "jq_l2", "zjw"]
    df = pandas.DataFrame()
    for name in industries:
        df_new = get_industries(name=name, date="2023-06-15")
        length = df_new.shape[0]
        print(df_new)
        industry_type = length * [name]
        print(industry_type)
        df_new.insert(len(df_new.columns), column='industry_type', value=industry_type)
        print(df_new)
        df = df._append(df_new)

    # print(df[['start_date']])
    industries_codes = list(df.index)
    df.insert(len(df.columns), column='industries_code', value=industries_codes)
    # # print(df)
    # df.to_excel('base_industry_info2.xlsx', sheet_name='base_industry_info',
    #             index=False)
    print(len(stocks))
    print(stocks)
    # # 获取贵州茅台("600519.XSHG")的所属行业数据
    # d = get_industry("600519.XSHG", date="2022-06-15")
    # # print(d)
    #
    # # 获取概念板块列表
    # df = get_concepts()[:5]
    # # print(df)
    #
    # # 获取风力发电概念板块的成分股
    # stocks = get_concept_stocks('SC0084',date="2022-07-15")
    # print(stocks[:5])
    #
    # # 查询股票所属概念
    # dict1 = get_concept('000001.XSHE', date='2019-07-15')
    # print(dict1)
