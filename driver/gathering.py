# -*- coding: utf-8 -*-
"""
Created on Thu Jan  2 11:29:32 2020

@author: giho9
"""

import pandas as pd
import os
from datetime import datetime
from dateutil.relativedelta import relativedelta
from pandas import ExcelWriter
from fredapi import Fred

fred = Fred(api_key='3b2795f81c94f1a105d1e4fc3661a45e')

def inspect_index_folder():
    if not os.path.exists(os.path.join(os.getcwd(), 'independent')):
        os.mkdir(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'independent'))
    folderpath = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'independent')
    return folderpath


def inspect_column_file():
    line = 'BAA,CSUSHPINSA,PCE,LREMTTTTUSM156S,DGORDER,TWEXBMTH,UNRATENSA,TCU,INDPRO,PPIACO,CPIAUCSL,HOUST,HSN1F,FEDFUNDS,USSLIND,TOTALSA,NEWORDER,UMCSENT,AMBNS,EXJPUS,EXKOUS,EXCHUS,T10Y2YM,XTEXVA01CNM667S,GACDFSA066MSFRBPHI,XTIMVA01KRM667S,KORPROINDMISMEI,KORCPIALLMINMEI,LRUNTTTTKRM156S,IR3TCD01KRM156N'
    index_list = list(map(str, (line.split(','))))
    return index_list

def Gathering():
    folderpath = inspect_index_folder()
    index_list = inspect_column_file()
    if index_list == False: return False
    
    time_point = datetime.strptime('2000-01-01', '%Y-%m-%d').date()
    
    #for index in index_list:
    for index in index_list:
        # Get data from fred
        df = fred.get_series_all_releases(index)
        #df_info = fred.search(index)
        
        # Drop column(realtime_start column)
        df.drop_duplicates( ["date"], keep="last", inplace=True)
        
        # Change column name
        df['DATE']=df['date'].dt.date
        df.rename(columns={'value':index}, inplace=True)
        
        # Column sort
        df = df[['DATE',index]]
        
        # Drop column(realtime_start column)
        df.drop(df[df.DATE < time_point].index, inplace=True)
        df.index = pd.RangeIndex(len(df.index))
        
        # Add empty row, Because we use shifted data and use it Machine-Learning
        df.loc[len(df), 'DATE'] = df['DATE'][len(df) - 1] + relativedelta(months=1)
        df.loc[len(df), 'DATE'] = df['DATE'][len(df) - 2] + relativedelta(months=2)
        df.loc[len(df), 'DATE'] = df['DATE'][len(df) - 3] + relativedelta(months=3)
        
        # Check for bad data
        try:
            df[index+'rate'] = (df[index] / df[index].shift(+1)) -1
            print(index,": success")
        except ZeroDivisionError:
            print(index,": error(data contained zero)")
            continue
        
        # Write to excel file
        df.to_excel(os.path.join(folderpath,index)+'.xlsx', sheet_name='Sheet1', index=False)
        #df_info.to_excel(writer, sheet_name='Sheet2', index=False)
    return True

result = Gathering()