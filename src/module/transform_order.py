# -*- coding: utf-8 -*-
"""
Created on Tue Aug 18 23:14:50 2020

@author: shyoo
"""
import os

import FinanceDataReader as fdr
import pandas as pd
import json

def ordering(odf, oc, on):
    order = pd.DataFrame()

    buy_filter = odf.buy == 1
    sell_filter = odf.sell == 1
    
    odf = odf[buy_filter | sell_filter]
    
    for _, row in odf.iterrows():
        
        od = row.Date
        
        if row.buy == 1: ot = 'buy'
        if row.sell == 1: ot = 'sell'

        try:
            pdf = fdr.DataReader(oc, row.Date, row.Date)
            op = str(int(pdf['Close']))
        except:
            op = str(0)
 
        olog = {"order_datetime": od,
        		 "order_type": ot,
        		 "item_code": oc,
        		 "item_name": on,
        		 "order_price": op,
        		 "order_option": 'all',
        		 "order_value": ''}
        
        order = order.append(olog, ignore_index='True')
        print(order)
    order = order[['order_datetime', 
                   'order_type', 
                   'item_code', 
                   'item_name', 
                   'order_price', 
                   'order_option', 
                   'order_value']]
    
    return order

def write_file(wdf, path, folder_name):
    if not os.path.exists(os.path.join(path, 'save')):
        os.mkdir(os.path.join(path, 'save'))
    save_path = os.path.join(path, 'save')
    if not os.path.exists(os.path.join(save_path, 'simulation')):
        os.mkdir(os.path.join(save_path, 'simulation'))
    save_path = os.path.join(save_path, 'simulation')
    if not os.path.exists(os.path.join(save_path, folder_name)):
        os.mkdir(os.path.join(save_path, folder_name))
    save_path = os.path.join(save_path, folder_name)
    wdict = wdf.to_dict(orient='record')
    with open(save_path+'/'+'order.json', 'w+', encoding='utf-8') as make_file:
        json.dump(wdict, make_file, ensure_ascii=False, indent='\t')

def run_transform_order(setting):
    df = pd.read_csv(setting['sim_file_path'])

    code = setting['etf_code']  # ETF 종목 코드
    name = setting['etf_name'] # ETF 종목 이름

    # 하나의 지수에 여러개의 ETF(지수펀드)가 존재하기 때문에
    # 어떤 ETF 종목으로 시뮬레이션 할지는 사용자가 정해야 함

    # example)
    # TIGER 미국나스닥100 - 133690
    # TIGER 미국S&P500 - 360750
    # TIGER 미국다우존스30 - 245340
    # TIGER 코스피 - 277630

    res = ordering(df, code, name)

    write_file(res, setting['path'], setting['save_folder_name'])

if __name__ == '__main__':
    
    df = pd.read_csv('완성!/test.csv')
    
    code = '133690' # ETF 종목 코드
    name = 'TIGER 미국나스닥100' # ETF 종목 이름
    
    # 하나의 지수에 여러개의 ETF(지수펀드)가 존재하기 때문에
    # 어떤 ETF 종목으로 시뮬레이션 할지는 사용자가 정해야 함
    
    # example)
    # TIGER 미국나스닥100 - 133690
    # TIGER 미국S&P500 - 360750
    # TIGER 미국다우존스30 - 245340
    # TIGER 코스피 - 277630
    
    res = ordering(df,code,name)
    
    write_file(res)