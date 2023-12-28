import pandas
from jqdatasdk import *
from pandas import DataFrame

if __name__ == '__main__':
    auth('18435205109', '407504@jun.')
    df = get_concepts()
    concept_codes = list(df.index)
    df = pandas.DataFrame()
    print(concept_codes)
    for concept_code in concept_codes:
        stocks = get_concept_stocks(concept_code, date='2022-06-24')
        # print(df_new)
        length = len(stocks)
        concept_codes_2 = length * [concept_code]
        dict1 = {'stocks': stocks, 'concept_code': concept_codes_2}
        df_new = pandas.DataFrame(dict1)
        df = pandas.concat([df, df_new])
    length= df.shape[0]
    df.insert(len(df.columns), column='base_date', value=length*['2022-06-24'])
    #     df_new.insert(len(df_new.columns), column='concept_code',
    #                   value=length*[concept_code])
    #     df = pandas.concat([df_new, df])
    print(df)
    df.to_excel('concept_stock.xlsx')
