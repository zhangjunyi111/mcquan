import pandas
from jqdatasdk import *
from pandas import DataFrame

if __name__ == '__main__':
    auth('13366248789', 'HONGhong1225')
    # industries = ["sw_l1", "sw_l2", "sw_l3", "jq_l1", "jq_l2", "zjw"]
    df = get_concepts()
    print(df)
    df.to_excel('concept_info.xlsx', sheet_name='concept_info')