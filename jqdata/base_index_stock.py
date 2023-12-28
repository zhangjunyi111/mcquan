import pandas
from jqdatasdk import *
from pandas import DataFrame

if __name__ == '__main__':
    auth('18435205109', '407504@Jun.')
    df = get_all_securities(types=['index'], date='2023-07-02')
    codes = list(df.index)
    print(codes)
    df = pandas.DataFrame()
    for code in codes:
        stocks = get_index_stocks(code, date='2023-07-02')
        dict = {'stock': stocks, "codes": len(stocks)*[code]}
        df_new = pandas.DataFrame(dict)
        df = pandas.concat([df, df_new])
    base_date = df.shape[0]*['2023-07-02']
    df.insert(len(df.columns), column='base_date', value=base_date)
    # print(df.shape[0])
    df.to_excel('index_stock20231125.xlsx', index=False)



    # mccode = list(df.index)
    # # print(df)
    # df.insert(len(df.columns), column='mccode', value=mccode)
    # df.to_excel('base_seurity_info.xlsx', sheet_name='base_seurity_info.xlsx',
    #             index=False)
    # df.to_excel('base_index_info.xlsx', sheet_name='base_index_info',
    #             index=False)
