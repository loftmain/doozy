# -*- coding: utf-8 -*-
"""
Created on Sun Jan  5 16:27:49 2020

@author: giho9
"""

import pandas_datareader.data as web
import pandas as pd
# pip install pandas_datareader
# pip install xlrd

def _hmbs(df, data, opt):
    status = False

    for _, row in df.iterrows():
        if row[opt[0]] == 1: # column opt
            year, month, day = row['Date'].year, row['Date'].month, row['Date'].day

            temp = data[data['year'] == year]
            temp = temp[temp['month'] == month]
            comp_v = temp['Adj Close'][temp.index[0]]

            for y, _ in temp.iterrows():

                if (temp['Adj Close'][y]/comp_v)-1 >= opt[1] and status == True: # n% opt
                    data['buy'][temp.index[0]] = 1
                    data['sell'][y] = 1
                    status = True
                    break

            if status == False:
                data['buy'][temp.index[0]] = 1
                data['sell'][temp.index[-1]] = 1
    return data

def input_df(path):
    df = pd.read_excel(path)
    df.rename(columns={'DATE': 'Date'}, inplace=True)
    df = pd.DataFrame(df, columns=['Date', 'HM4UP_predict'])
    return df

def calculate_date(df):
    start = df['Date'][0]
    end = df['Date'][len(df) - 1]
    return start, end

def read_df_from_yahoo(index):
    data = web.DataReader(index, 'yahoo', start, end)
    data = data.reset_index()
    data['year'] = data["Date"].apply(lambda x: x.year)
    data['month'] = data["Date"].apply(lambda x: x.month)
    data['buy'] = 0
    data['sell'] = 0

if __name__ == '__main__':

    path = 'dependent/^DJI.xlsx' # form에서 입력받음
    df = input_df(path)

    start, end = calculate_date(df)
    index = '^DJI' # form에서 입력받음

    yahoo = read_df_from_yahoo(index)
    strategy = 'HMBS'
    # 전략종류
    # HMBS : hm n up에 월초매수 후, n% 상승시 매도 [완성]
    # HMBLS : hm n up에 월초매수 후, 월말에 매도 [완성]
    # LMBS : lm n dn에 등장일에 매수 후 보유. hmup 월에 특정일에 매도 [미완성]
    # LMBLS : lm n dn에 마지막일에 매수 후 보유. hmup 월 마지막일에 매도 [미완성]

    if strategy == ' HMBS':
        result = _hmbs(df, yahoo, ['HM4UP_predict', 0.4])

    result.to_excel('input_order.xlsx', header=True, index=False)
