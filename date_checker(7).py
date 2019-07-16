import os
import pandas as pd
import numpy as np

def max_date():
    base_dir = os.getcwd() + '/data/csv/'
    dlist = {}
    for file in os.listdir(base_dir):
        filename = os.fsdecode(file)
        if filename.endswith(".csv") and filename not in ['indian_stations.csv', 'max_val_dump(do not delete).csv', 'cols_dump(do not delete).csv','selection_list.csv']:
            df = pd.DataFrame()
            with open(base_dir + filename) as csv:
                df = pd.read_csv(csv, index_col=None)
                dlist[max(df['YEARMODA'].tolist())] = 1
    dlist = list(dlist.keys())
    if(len(dlist)==1):
        return dlist[0]
    else:
        return -1 #more than one max date
print(max_date())

