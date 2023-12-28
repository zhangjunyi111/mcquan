# # 获取计算机/互联网行业的成分股
import pandas
from jqdatasdk import *
from pandas import DataFrame

if __name__ == '__main__':
    auth('13366248789', 'HONGhong1225')

    df = get_all_securities(
        types=['stock'],
        date='2023-09-10')
    mccode = list(df.index)
    # print(df)
    df.insert(len(df.columns), column='mccode', value=mccode)
    df.to_excel('base_seurity_info5.xlsx', sheet_name='base_seurity_info.xlsx',
                index=False)