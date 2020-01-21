# -*- coding: utf-8 -*-
"""
Created on Thu Jan  2 11:29:32 2020

@author: giho9
"""

import pandas as pd
import os
import pandas_datareader.data as web
from datetime import datetime
from dateutil.relativedelta import relativedelta
from fredapi import Fred

def inspect_index_folder():
    '''
    independent 폴더가 존재하는지 확인하는 함수
    independent 폴더가 존재한다면 생성하지 않는다.
    independent 폴더가 존재하지 않는다면 생성한다.
    
    [입력]
    없음
    
    [출력]
    independent 폴더 경로
    '''
    if not os.path.exists(os.path.join(os.getcwd(), 'independent')):
        os.mkdir(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'independent'))
    folderpath = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'independent')
    return folderpath

def inspect_column_file():
    '''
    fred로부터 받을 경제지표들이 적혀있는 
    ../save/column.txt경로에 파일이 존재하는지 확인하는 함수
    column.txt파일의 내용은 다음과 같다
    
    [example]
    BAA, HOUST, CSUSHPINSA
    콤마로 구분되어있으며 한 줄에 모두 작성하면 된다.
    
    [입력]
    없음
    
    [출력]
    fred로부터 받을 경제지표들의 약자들이 인덱스로 있는 리스트
    '''
    if not os.path.join(os.path.dirname(os.path.realpath(__file__)), 'save/column.txt'):    
        print('column option file does not exist')     
        return False
    f = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'save/column.txt'), 'r')
    line = f.readline()
    index_list = list(map(str, (line.split(','))))
    return index_list

def Gathering_independent(key, start):
    '''
    column.txt에 지정되어있는 경제지표들을 fred로부터 받아온다.
    
    [입력]
    fred private api key
    시작 날짜
    
    [출력]
    경제지표 파일들(csv file)
    '''
    folderpath = inspect_index_folder()
    index_list = inspect_column_file()
    if not index_list:
        return False
    
    time_point = datetime.strptime(start, '%Y-%m-%d').date()
    #time_point = time_point+timedelta(days=-1)
    
    for index in index_list:
        
        # Get data from fred
        df = Fred.get_series_all_releases(index)
        #df_info = fred.search(index)
        
        # Drop column(realtime_start column)
        df.drop_duplicates( ["date"], keep="last", inplace=True)
        
        # Change column name
        df['Date']=df['date'].dt.date
        df.rename(columns={'value':index}, inplace=True)
        
        # Column sort
        df = df[['Date',index]]
        
        # Drop column(realtime_start column)
        df.drop(df[df.Date < time_point].index, inplace=True)
        df.index = pd.RangeIndex(len(df.index))
        
        # Add empty row, Because we use shifted data and use it Machine-Learning
        df.loc[len(df), 'Date'] = df['Date'][len(df) - 1] + relativedelta(months=1)
        df.loc[len(df), 'Date'] = df['Date'][len(df) - 2] + relativedelta(months=2)
        df.loc[len(df), 'Date'] = df['Date'][len(df) - 3] + relativedelta(months=3)
        
        # Check for bad data
        try:
            df[index+'rate'] = (df[index] / df[index].shift(+1)) -1
            print(index,": success")
        except ZeroDivisionError:
            print(index,": error(data contained zero)")
            continue
        df = df.drop(0,0)
        # Write to excel file
        df.to_csv(os.path.join(folderpath,index)+'.csv', index=False)
        #df_info.to_excel(writer, sheet_name='Sheet2', index=False)

def Gathering_dependent(code, start, end, path):
    '''
    yahoo finance로부터 종목데이터 or 지수데이터를 받아온다.
    
    [입력]
    종목코드 or 지수이름
    시작날짜
    끝날짜
    지정경로
    '''
    try:
        df = \
        web.DataReader(code, 'yahoo', start, end)
        df = df.reset_index()
    except(KeyError):
        return False
    
    df.to_csv(path+code+'.csv', index=False)
    
if __name__ == '__main__':
    
# 독립변수=====================================================================
#     code = '^DJI' # form에서 입력받음
#     start = '2010-01-01' # form에서 입력받음
#     end = '2019-12-31' # form에서 입력받음
#     path = 'dependent/'
#     Gathering_dependent(code, start, end)
# =============================================================================

# 종속변수=====================================================================
#     key = Fred(api_key='3b2795f81c94f1a105d1e4fc3661a45e') # form에서 입력받음
#     start = '2010-01-01' # form에서 입력받음
#     Gathering_independent(key, start)
# =============================================================================
    