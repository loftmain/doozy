#!/usr/bin/env python
# coding: utf-8

import datetime

import matplotlib.pyplot as plt
import numpy
import pandas_datareader.data as wb
import talib

__author__ = 'Jinjae Lee <leejinjae7@gmail.com>'

# Download data from yahoo finance
start = datetime.datetime(2010, 1, 1)
end = datetime.datetime(2014, 3, 24)
ticker = "AAPL"
f = wb.DataReader(ticker, 'yahoo', start, end)

f['SMA_20'] = talib.SMA(numpy.asarray(f['Close']), 20)
f['SMA_50'] = talib.SMA(numpy.asarray(f['Close']), 50)
f.plot(y=['Close', 'SMA_20', 'SMA_50'], title='AAPL Close & Moving Averages')
ax1 = plt.plot(f.index, f.Close)
ax1 = plt.plot(f.index, f.SMA_20)
ax1 = plt.plot(f.index, f.SMA_50)
plt.show()
print(f)
