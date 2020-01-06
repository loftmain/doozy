# -*- coding: utf-8 -*-
"""
Created on Sun Jan  5 16:27:49 2020

@author: giho9
"""

import pandas_datareader.data as web
import pandas as pd
# pip install pandas_datareader

df = pd.read_excel('input_order.xlsx')
df.rename(columns = {'DATE':'Date'}, inplace=True)
df = pd.DataFrame(df, columns=['Date', 'HM4UP_predict'])

start = df['Date'][0]
end = df['Date'][len(df)-1]

data = web.DataReader('^DJI', 'yahoo', start, end)
data = data.reset_index()
data['year'] = data["Date"].apply(lambda x: x.year)
data['month'] = data["Date"].apply(lambda x: x.month)
data['buy'] = 0
data['sell'] = 0
status = False

for x, row in df.iterrows():
    if row['HM4UP_predict'] == 1:
        year, month, day = row['Date'].year, row['Date'].month, row['Date'].day
        
        temp = data[data['year'] == year]
        temp = temp[temp['month'] == month]
        comp_v = temp['Adj Close'][temp.index[0]]
        
        for y, _ in temp.iterrows():
           
            if temp['Adj Close'][y]/comp_v >= 1.04:
                data['buy'][temp.index[0]] = 1
                data['sell'][y] = 1
                status = True
                break
            
        if status == False:
            data['buy'][temp.index[0]] = 1
            data['sell'][temp.index[-1]] = 1
data.to_excel('test.xlsx', index=False, header=True)

