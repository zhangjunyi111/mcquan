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
        df_new = get_index_weights(index_id=code, date='2023-07-02')
        df_new.insert(len(df_new.columns), column='index',
                      value=df_new.shape[0]*[code])
        df = pandas.concat([df, df_new])
    # base_date = df.shape[0]*['2023-07-02']
    # df.insert(len(df.columns), column='base_date', value=base_date)
    print(df.shape[0])
    stocks = list(df.index)
    df.insert(len(df.columns), column='stocks', value=stocks)
    df.to_excel('index_stock_weight.xlsx', index=False)