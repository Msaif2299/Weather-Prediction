import os
import warnings
import csv
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from statsmodels.tsa.vector_ar.var_model import VAR, VARResults
from statsmodels.tsa.vector_ar.vecm import coint_johansen
from sklearn.metrics import mean_squared_error
from statsmodels.iolib.smpickle import load_pickle

COLUMNS = ['TEMP', 'DEWP', 'SLP', 'STP', 'VISIB', 'WSP', 'MXSPD', 'GUST', 'MAX', 'MIN', 'PRCP', 'SNDP']
warnings.filterwarnings("ignore")
def get_predictions(station_number, number_of_predictions):
    base_dir = os.getcwd() + '/data/'
    try:
        model = load_pickle(base_dir + 'models/' + str(station_number) + '.pkl')
    except FileNotFoundError as e:
        print("Model not found. Please run this script atleast once.")
        return None
    yhat = model.forecast(model.y, steps = number_of_predictions)
    max_vals = []
    columns = []
    try:
        max_val_file_content = list(csv.reader(open(base_dir + "csv/max_val_dump(do not delete).csv", 'r')))
    except FileNotFoundError as e:
        print("CSV file for maximum values dumped not found. Please run the script to create it.")
        return None
    try:
        columns_file_content = list(csv.reader(open(base_dir + "csv/cols_dump(do not delete).csv", 'r')))
    except FileNotFoundError as e:
        print("CSV file for columns dumped not found. Please run the script to create it.")
        return None
    for line in max_val_file_content:
        if str(line[0]) == str(station_number)[:-1]:
            max_vals = list(map(float, line[1:]))
            break
    yhat = yhat * [max_vals]
    for line in columns_file_content:
        if str(line[0]) == str(station_number)[:-1]:
            columns = line[1:]
            break
    cols_to_return = {}
    for key in COLUMNS:
        if key in columns:
            cols_to_return[key] = []
            index = columns.index(key)
            for row in yhat:
                cols_to_return[key].append('{:.2f}'.format(row[index]))
        else:
            cols_to_return[key] = None
    return cols_to_return


if __name__ == '__main__':
    base_dir = os.getcwd() + '/data/'
    if not os.path.exists(base_dir + 'models'):
        os.mkdir(base_dir + 'models')
    try:
        max_val_writer = csv.writer(open(base_dir + "csv/max_val_dump(do not delete).csv", 'w', newline=''))
        col_writer = csv.writer(open(base_dir + "csv/cols_dump(do not delete).csv", 'w', newline=''))
    except PermissionError as e:
        print("Failure to create files. Time to exit.")
        exit()

    for file in os.listdir(base_dir + 'csv/'):
        filename = os.fsdecode(file)
        if filename.endswith(".csv") and filename not in ['indian_stations.csv', 'max_val_dump(do not delete).csv', 'cols_dump(do not delete).csv', 'selection_list.csv']:
            print("On ---> {}".format(filename), end = ' ')
            train = pd.read_csv(base_dir + filename)
            train.drop(columns=['STN---', 'WBAN'], inplace=True)
            train.index = train['YEARMODA']
            train['Dates'] = pd.to_datetime(train['YEARMODA'].astype(str), format='%Y%m%d')
            train.index = train['Dates']
            train.drop(columns=['YEARMODA', 'Dates', 'TEMP OBS', 'DEWP OBS', 'SLP OBS', 'STP OBS', 'VISIB OBS', 'WDSP OBS', 'FRSHTT'], inplace=True)
            for col in ['MAX', 'MIN']:
                train[col] = train[col].map(lambda x: x.rstrip('*'))
                train[col] = train[col].replace('9999.9', np.nan)
                train[col] = train[col].astype(float)
            for col in ['TEMP', 'DEWP', 'SLP', 'STP']:
                train[col] = train[col].replace(9999.9, np.nan)
            for col in ['VISIB', 'WDSP', 'MXSPD', 'GUST', 'SNDP']:
                train[col] = train[col].replace(999.9, np.nan)
            print('25%', end = ' ')
            col = 'PRCP'
            train[col] = train[col].map(lambda x: x.rstrip('ABCDEFGHI'))
            train[col] = train[col].astype(float)
            train[col] = train[col].replace(99.99, 0)
            train = train.fillna(method='ffill')
            print('50%', end = ' ')
            cols_to_drop = []
            columns = train.columns
            for col in columns:
                if train[col].isnull().sum() != 0:
                    cols_to_drop.append(col)
            train.drop(columns = cols_to_drop, inplace=True)
            max_vals = train.max()
            train = train/train.max().astype(float)
            print('75%', end = ' ')
            training = train[:int(0.8*len(train))]
            validation = train[int(0.8*len(train)):]
            model = VAR(endog = train)
            model_fit = model.fit()
            model_fit.save(base_dir + 'models/' + filename.split('.')[0] + '0.pkl')
            temp = [val for val in max_vals]
            temp.insert(0, str(filename.split('.')[0]))
            max_val_writer.writerow(temp)
            temp = [col for col in train.columns]
            temp.insert(0, str(filename.split('.')[0]))
            col_writer.writerow(temp)
            print('100%')
