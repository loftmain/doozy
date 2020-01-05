# -*- coding: utf-8 -*-
"""
Created on Sun Jan  5 16:27:49 2020

@author: giho9
"""

import pandas_datareader.data as web
import datetime
import matplotlib.pyplot as plt
# pip install pandas_datareader

start = datetime.datetime(2010, 1, 1)
end = datetime.datetime(2019, 12, 31)

data = web.DataReader('^DJI', 'yahoo', start, end)