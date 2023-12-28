import pandas
from jqdatasdk import *
from pandas import DataFrame

if __name__ == '__main__':
    auth('18435205109', '407504@Jun.')
    df = get_all_securities(types=['index'], date='2023-09-10')
    mccode = list(df.index)
    # # print(df)
    df.insert(len(df.columns), column='index_code', value=mccode)
    df.to_excel('base_seurity_info_with_mccode.xlsx',
                sheet_name='base_seurity_info_with_mccode.xlsx',
                index=False)
    # df.to_excel('base_index_info.xlsx', sheet_name='base_index_info',
    #             index=False)
