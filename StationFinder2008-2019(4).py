import os
import gzip as gz
import pandas as pd
import numpy as np
base_dir = os.getcwd() + '/data/'
csv_file_saver_dir = base_dir + 'csv'
if not os.path.exists(csv_file_saver_dir):
    os.mkdir(csv_file_saver_dir)
looping_year = 2008
end_year = 2019
file_stns = [i for i in range(42001, 42999)]+[j for j in range(43001, 43400)]
columns = ['STN---', 'WBAN', 'YEARMODA', 'TEMP', 'TEMP OBS', 'DEWP', 'DEWP OBS', 'SLP', 'SLP OBS', 'STP', 'STP OBS', 'VISIB', 'VISIB OBS', 'WDSP', 'WDSP OBS', 'MXSPD', 'GUST', 'MAX', 'MIN', 'PRCP', 'SNDP', 'FRSHTT']
for file in os.listdir(csv_file_saver_dir + '/'):
    filename = os.fsdecode(file)
    if filename.endswith(".csv"):
        os.remove(base_dir + filename)
        print(f"{filename} removed")
while looping_year <= end_year:
    print(f"In year, {looping_year}")
    dirname = f'gsod_{looping_year}/'
    new_dir = base_dir + dirname
    for stn in file_stns:
        filename = new_dir + f'{stn}0-99999-{looping_year}.op.gz'
        try:
            with gz.open(filename, 'r') as g:
                file_content = g.read()
                data = np.array([str(x.decode("utf-8")) for x in file_content.split()][16:]).reshape(-1, 22)
                df = pd.DataFrame(data)
                df.columns= columns
                df['FRSHTT'] = df['FRSHTT'].astype('str')
                with open(csv_file_saver_dir + '/' + f'{stn}' + '.csv', 'a', newline='') as w:
                    header = None
                    if w.tell() == 0:
                        header = columns
                    df.to_csv(w, header = header, index = None)
        except FileNotFoundError as e:
            pass
    looping_year += 1