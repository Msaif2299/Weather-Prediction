import os
import pandas as pd
import numpy as np
indian_stn_numbers = [i for i in range(42001, 42999)]+[j for j in range(43001, 43400)]
with open(os.getcwd() + "/data/isd-history.txt", 'r') as his:
    file_content = his.read().splitlines()[20:]
    headers = file_content[0].split()
    file_content.pop(1)
    file_content.pop(0)
    data = []
    for line in file_content:
        data.append(line.split())
    data = np.array(data)
    file_content = []
    count = 0
    for line in data:
        try:
            stn = int(line[0])
            if (stn >= 420010 and stn <= 429990) or (stn >= 430010 and stn <= 434000):
                file_content.append(line)
                count += 1
        except ValueError as e:
            pass
    file_content = file_content[:-2]
    new_file_content = []
    count = 0
    for line in file_content:
        if (len(line) == 4 or len(line) == 7) or int(line[0])%10 != 0:
            file_content.pop(count)
        else:
            temp = line[:-5]
            temp.pop(1)
            if temp[-1] != 'IN':
                temp.pop()
            temp.pop()
            if temp[-1] == '&':
                temp.pop()
            if temp[-1][-1] == '&':
                temp[-1] = temp[-1][:-1]
            formatted_temp = [None]*2
            formatted_temp[0] = temp[0]
            formatted_temp[1] = ' '.join(temp[1:])
            new_file_content.append(formatted_temp)
            print(*formatted_temp)
        count += 1
    new_file_content = np.array(new_file_content)
    df = pd.DataFrame(new_file_content)
    with open(os.getcwd() + '/data/indian_stations.csv', 'w', newline = '') as w:
        df.to_csv(w, index = None, header = ['STN---', 'Name'])