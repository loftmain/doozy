# -*- coding: utf-8 -*-
"""
Created on Mon Jan  6 15:49:26 2020

@author: giho9
"""

import pandas_datareader.data as web
import datetime
import matplotlib.pyplot as plt
from zipline.api import order_target, record, symbol
from zipline.algorithm import TradingAlgorithm
import pandas as pd

# ========================================================================
'''
start = datetime.datetime(2017, 1, 1)
end = datetime.datetime(2019, 12, 31)
data = web.DataReader("AAPL", "yahoo", start, end)
 
data = data[['Adj Close']]
data.columns = ['AAPL']
data = data.tz_localize('UTC')
'''
# =============================================================================

data = pd.read_excel('test.xlsx')
data = pd.DataFrame(data, columns=['Date', 'Adj Close', 'buy', 'sell'])
data.set_index(data['Date'], inplace=True)
data = data.tz_localize('UTC')

def initialize(context):
    context.i = 0
    context.sym = symbol('Adj Close')
    #context.hold = False

def handle_data(context, data):
    order_target(context.sym, 1)
    '''
    context.i += 1
    if context.i < 20:
        return

    buy = False
    sell = False

    ma5 = data.history(context.sym, 'price', 5, '1d').mean()
    ma20 = data.history(context.sym, 'price', 20, '1d').mean()
    
    if ma5 > ma20: # and context.hold == False:
        order_target(context.sym, 100) # 현재 시점에서 100개 거래 타겟 설정
        #context.hold = True
        buy = True # buy status를 true로 설정
    elif ma5 < ma20:# and context.hold == True:
        order_target(context.sym, -100) # 현재 시점에서 100개 거래 타겟 설정
        #context.hold = False
        sell = True # sell status를 true로 설정

    record(AAPL=data.current(context.sym, "price"), buy=buy, sell=sell)
    # record로 거래기록하기???
    '''
    
algo = TradingAlgorithm(initialize=initialize, handle_data=handle_data)
result = algo.run(data)
result = result[['starting_cash', 'ending_cash', 'ending_value']]
