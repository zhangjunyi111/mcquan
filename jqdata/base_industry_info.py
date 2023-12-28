# 获取2020-05-07当天证监会行业行业列表
import pandas
import pandas as pd
from jqdatasdk import *
from pandas import DataFrame

if __name__ == '__main__':
    auth('18435205109', '407504@Jun.')
    industries = ["sw_l1", "sw_l2", "sw_l3", "jq_l1", "jq_l2", "zjw"]
    df = pandas.DataFrame()
    for name in industries:
        df_new = get_industries(name=name, date='2023-08-24')
        length = df_new.shape[0]
        industry_type = length * [name]
        df_new.insert(len(df_new.columns), column='industry_type', value=industry_type)
        df = pd.concat([df,df_new])
    df.to_excel('base_industry_info20231125.xlsx')