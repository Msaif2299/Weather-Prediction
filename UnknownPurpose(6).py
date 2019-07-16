import os
import pandas as pd
import numpy as np

base_dir = os.getcwd() + '/'
for file in os.listdir(base_dir + 'data/csv/'):
    filename = os.fsdecode(file)
    if filename.endswith(".csv") and filename not in ["indian_stations.csv", "max_val_dump(do not delete).csv", "cols_dump(do not delete).csv", "selection_list.csv"]:
        df = pd.DataFrame()
        with open(base_dir + filename) as csv:
            df = pd.read_csv(csv, index_col=None)
        if len(df) < 4000:
            os.remove(base_dir + filename)
            print(f"{filename} removed")
station_info = pd.DataFrame()
station_info = pd.read_csv(base_dir + "data/csv/indian_stations.csv", index_col=None)
count = 0
miss = 0
new_file_content=[]
values = station_info['Name'].tolist()
keys = station_info['STN---'].tolist()
station_list = dict(zip(keys,values))
for file in os.listdir(base_dir + 'data/csv/'):
    filename = os.fsdecode(file)
    if filename.endswith(".csv") and filename not in ["indian_stations.csv", "max_val_dump(do not delete).csv", "cols_dump(do not delete).csv", "selection_list.csv"]:
        stn_name = filename.split('.')[0]
        if int(stn_name)*10 in station_info['STN---'].tolist():
            formatted_temp = [None]*2
            formatted_temp[0] = int(stn_name)*10
            formatted_temp[1] = station_list[int(stn_name)*10]
            new_file_content.append(formatted_temp)
            print(*formatted_temp)
        else:
            os.remove(base_dir + 'data/csv/' + filename)
            print(f"{stn_name} removed")
            miss += 1
        count += 1
print(f"Fails: {miss}/{count}")
new_file_content = np.array(new_file_content)
df = pd.DataFrame(new_file_content)
with open(base_dir + 'data/csv/selection_list.csv', 'w', newline = '') as w:
        df.to_csv(w, index = None, header = ['STN---', 'Name'])