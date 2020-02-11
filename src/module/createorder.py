# -*- coding: utf-8 -*-
"""
Created on Sun Jan  5 16:27:49 2020

@author: giho9
"""
import datetime
import os

import pandas as pd
import pandas_datareader.data as web

from src.module.io import set_save_folder

# pip install pandas_datareader
# pip install xlrd

pd.options.mode.chained_assignment = None


def _hmbs(df, data, opt):
    status = False

    for _, row in df.iterrows():
        if row[opt[0]] == 1: # column opt
            datetime_obj = datetime.datetime.strptime(row['Date'], '%Y-%m-%d %H:%M:%S')

            year, month, day = datetime_obj.year, datetime_obj.month, datetime_obj.day
            temp = data[data['year'] == year]
            temp = temp[temp['month'] == month]
            #temp = temp.reset_index()
            print(year, month, row)
            # 현재 기준 마지막달 까지 할 경우 오류남
            if (year == 2020) and (month == 1):
                break
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

def _lmbs(df, data, opt):
    status = False

    for _, row in df.iterrows():
        if row[opt[0]] == 0:  # column opt
            datetime_obj = datetime.datetime.strptime(row['Date'], '%Y-%m-%d %H:%M:%S')

            year, month, day = datetime_obj.year, datetime_obj.month, datetime_obj.day

            temp = data[data['year'] == year]
            temp = temp[temp['month'] == month]
            comp_v = temp['Adj Close'][temp.index[0]]

            for y, _ in temp.iterrows():

                if (temp['Adj Close'][y] / comp_v) - 1 <= opt[1] and status == True:  # n% opt
                    data['buy'][temp.index[0]] = 1
                    data['sell'][y] = 1
                    status = True
                    break

            if status == False:
                data['buy'][temp.index[0]] = 1
                data['sell'][temp.index[-1]] = 1
    return data


def input_df(path, column):
    df = pd.read_csv(path)
    df = pd.DataFrame(df, columns=['Date', column])
    return df


def calculate_date(df):
    start = df['Date'][0]
    end = df['Date'][len(df) - 1] # 마지막 달이 최신 월일 경우 에러 발생
    return start, end


def read_df_from_yahoo(index, start, end):
    data = web.DataReader(index, 'yahoo', start, end)
    data = data.reset_index()
    data['year'] = data["Date"].apply(lambda x: x.year)
    data['month'] = data["Date"].apply(lambda x: x.month)
    data['buy'] = 0
    data['sell'] = 0
    return data


def run_create_order(setting):
    global result
    option = [setting['column_name'], setting['per']]  # [컬럼이름과, 비율]
    df = input_df(setting['order_file_path'], setting['column_name'])
    start, end = calculate_date(df)
    index = setting['yahoo_code']
    yahoo = read_df_from_yahoo(index, start, end)
    strategy = setting['strategy']
    # 전략종류
    # HMBS : hmup이 1일 때, 월초 매수하여 월중 n%상승 등장일에 매도
    # HMBLS : hmup이 1일 때, 월초 매수하여 월말에 매도
    # LMBS : lmdn이 0일 때, 월초 매수하여 월중 n%상승 등장일에 매도
    # LMBLS : lmdn이 0일 때, 월초 매수하여 월말에 매도

    if strategy == 'HMBS':
        result = _hmbs(df, yahoo, option)  # form에서 입력받음 [컬럼이름과, 비율]
    elif strategy == 'HMBLS':
        result = _hmbs(df, yahoo, option)  # form에서 입력받음 [컬럼이름과, 비율]
    elif strategy == 'LMBS':
        result = _lmbs(df, yahoo, option)  # form에서 입력받음[컬럼이름과, 비율]
    elif strategy == 'LMBNS':
        result = _lmbs(df, yahoo, option)  # form에서 입력받음[컬럼이름과, 비율]

    save_path = set_save_folder(os.curdir, 'order')
    result.to_csv(save_path + '/' + setting['save_name'], header=True, index=False)


if __name__ == '__main__':

    path = 'D:\\modeling\\save\\modeling\\a.csv'  # form에서 입력받음 [파일경로]
    option = ['HM2UP_predict', 0.02]  # [컬럼이름과, 비율]
    # HMBLS, LMBLS는 option[1]에 math.inf를 삽입하면됨

    df = input_df(path, option[0])
    start, end = calculate_date(df)
    index = '^GSPC'  # form에서 입력받음
    print(start, end)
    yahoo = read_df_from_yahoo(index, start, end)
    strategy = 'HMBS'  # form에서 입력받음 [전략]
    print(yahoo)

    # 전략종류
    # HMBS : hmup이 1일 때, 월초 매수하여 월중 n%상승 등장일에 매도
    # HMBLS : hmup이 1일 때, 월초 매수하여 월말에 매도
    # LMBS : lmdn이 0일 때, 월초 매수하여 월중 n%상승 등장일에 매도
    # LMBLS : lmdn이 0일 때, 월초 매수하여 월말에 매도

    if strategy == 'HMBS':
        result = _hmbs(df, yahoo, option) # form에서 입력받음 [컬럼이름과, 비율]
    elif strategy == 'HMBLS':
        result = _hmbs(df, yahoo, option) # form에서 입력받음 [컬럼이름과, 비율]
    elif strategy == 'LMBS':
        result = _lmbs(df, yahoo, option) # form에서 입력받음[컬럼이름과, 비율]
    elif strategy == 'LMBNS':
        result = _lmbs(df, yahoo, option) # form에서 입력받음[컬럼이름과, 비율]

    result.to_excel('D:\\modeling\\save\\a.xlsx', header=True, index=False)
