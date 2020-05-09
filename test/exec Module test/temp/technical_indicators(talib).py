# -*- coding: utf-8 -*-
"""
Created on Mon Jan 20 21:33:52 2020

@author: shyoo
"""
# Overlap Studies
# =============================================================================
# BBANDS               Bollinger Bands
# DEMA                 Double Exponential Moving Average
# EMA                  Exponential Moving Average
# HT_TRENDLINE         Hilbert Transform - Instantaneous Trendline
# KAMA                 Kaufman Adaptive Moving Average
# MA                   Moving average
# MAMA                 MESA Adaptive Moving Average
# MAVP                 Moving average with variable period
# MIDPOINT             MidPoint over period
# MIDPRICE             Midpoint Price over period
# SAR                  Parabolic SAR
# SAREXT               Parabolic SAR - Extended
# SMA                  Simple Moving Average
# T3                   Triple Exponential Moving Average (T3)
# TEMA                 Triple Exponential Moving Average
# TRIMA                Triangular Moving Average
# WMA                  Weighted Moving Average
# =============================================================================
# Momentum Indicators
# =============================================================================
# ADX                  Average Directional Movement Index
# ADXR                 Average Directional Movement Index Rating
# APO                  Absolute Price Oscillator
# AROON                Aroon
# AROONOSC             Aroon Oscillator
# BOP                  Balance Of Power
# CCI                  Commodity Channel Index
# CMO                  Chande Momentum Oscillator
# DX                   Directional Movement Index
# MACD                 Moving Average Convergence/Divergence
# MACDEXT              MACD with controllable MA type
# MACDFIX              Moving Average Convergence/Divergence Fix 12/26
# MFI                  Money Flow Index
# MINUS_DI             Minus Directional Indicator
# MINUS_DM             Minus Directional Movement
# MOM                  Momentum
# PLUS_DI              Plus Directional Indicator
# PLUS_DM              Plus Directional Movement
# PPO                  Percentage Price Oscillator
# ROC                  Rate of change : ((price/prevPrice)-1)*100
# ROCP                 Rate of change Percentage: (price-prevPrice)/prevPrice
# ROCR                 Rate of change ratio: (price/prevPrice)
# ROCR100              Rate of change ratio 100 scale: (price/prevPrice)*100
# RSI                  Relative Strength Index
# STOCH                Stochastic
# STOCHF               Stochastic Fast
# STOCHRSI             Stochastic Relative Strength Index
# TRIX                 1-day Rate-Of-Change (ROC) of a Triple Smooth EMA
# ULTOSC               Ultimate Oscillator
# WILLR                Williams' %R
# =============================================================================

import pandas as pd
import numpy as np
import talib.abstract as ta
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import mpl_finance


def _bb(x, w, k):
    """
    Calculate Bollinger Bands
    ubb = MA_w(x) + k * sd(x)
    mbb = MA_w(x)
    lbb = MA_w(x) - k * sd(x)
    
    :sd: 표준편차
    
    :param x: 수정종가 시리즈
    :param w: window size
    :param k: 볼린저 밴드에서 고려하는 상수로 볼린저 밴드의 넓이
    
    :return: (ubb, mbb, lbb)
    """
    x = pd.Series(x)
    mbb = x.rolling(w).mean()
    ubb = mbb + k * x.rolling(w).std()
    lbb = mbb - k * x.rolling(w).std()
    
    return ubb, mbb, lbb

def _sma(x, w):
    """
    Calculate Simple Moving Average
    ma5 = n1 + n2 .....n5 / 5
    ma10 = n1 + n2 .....n10 / 10
    ma20 = n1 + n2 .....n20 / 20
    
    :n1: 윈도우 사이즈 내의 1행 종가
    :n5: 윈도우 사이즈 내의 5행 종가
    
    :param x: 수정종가 시리즈
    :param w: window size
    
    return (ma)
    """
    x = pd.Series(x)
    sma = x.rolling(w).mean()
    
    return sma

def _ema(x, w):
    """
    Calculate Exponetial Moving Average
    
    금일의 지수이동평균 = (금일 종가 * EP) + (전일의 지수 이동평균 * (1 - EP))
    EP(평활 계수 : Exponential Percentage) = 2 / (기간 + 1)
    
    :param x: 수정종가 시리즈
    :param w: window size
    
    return (ema)
    """
    ema = x.ewm(span=w).mean()
    
    return ema

def weighted_mean(weight_array):
    def inner(x):
        return (weight_array * x).mean()
    return inner

def _wma(x, w):
    """
    Calculate Weighted Moving Average
    
    선형 가중 이동평균(Linearly Weighted Moving Average)을 보면 동일한 값 
    1(4일 전) 2(3일 전) 3(2일 전) 4(1일 전) 5(금일)의 가격이라면 금일의 종가에 
    가중치를 부여하여 1*1 + 2*2 + 3*3 + 4*4 + 5*5 = 55

    계산에서 사용된 값 (1 + 2 + 3 + 4 + 5 = 15)

    55 / 15 = 3.67을 5개의 값의 평균으로 사용

    :param x: 수정종가 시리즈
    :param w: window size
    
    return (wma)
    """
    weights = np.arange(1,w+1)
    wma = x.rolling(w).apply(lambda prices: np.dot(prices, weights)/weights.sum(), raw=True)
    
    return wma

if __name__ == '__main__':
    
    df = pd.read_csv('dependent/^DJI.csv') \
    .dropna(how='all') \
    .rename(columns=lambda col:col.lower())

    # bb = _bb(df['Adj Close'], 20, 2)
    # sma = _sma(df['close'], 5)
    # ema = _ema(df['close'], 30)
    # wma = _wma(df['Adj Close'], 5)

    #BBANDS - Bollinger Bands
    bb = ta.BBANDS(df, timeperiod=5, nbdevup=2, nbdevdn=2, matype=0)
    
    #DEMA - Double Exponential Moving Average
    dema = ta.DEMA(df, timeperiod=30)
    
    #EMA - Exponential Moving Average
    ema = ta.EMA(df, timeperiod=30)
    
    #HT_TRENDLINE - Hilbert Transform - Instantaneous Trendline
    ht = ta.HT_TRENDLINE(df)
    
    #KAMA - Kaufman Adaptive Moving Average
    kama= ta.KAMA(df, timeperiod=30)
    
    #MA - Moving average
    ma = ta.MA(df, timeperiod=30, matype=0)
    
    #MAMA - MESA Adaptive Moving Average
    #mama, fama = ta.MAMA(df, fastlimit=0, slowlimit=0)
    
    #MAVP - Moving average with variable period
    #mavp = ta.MAVP(df, minperiod=2, maxperiod=30, matype=0)
    
    #MIDPOINT - MidPoint over period
    mpt = ta.MIDPOINT(df, timeperiod=14)
    
    #MIDPRICE - Midpoint Price over period
    mpr = ta.MIDPRICE(df, timeperiod=14)
    
    #SAR - Parabolic SAR
    sar = ta.SAR(df, acceleration=0, maximum=0)
    
    #SAREXT - Parabolic SAR - Extended
    sarext = ta.SAREXT(df, startvalue=0, offsetonreverse=0, accelerationinitlong=0, accelerationlong=0, accelerationmaxlong=0, accelerationinitshort=0, accelerationshort=0, accelerationmaxshort=0)
    
    #SMA - Simple Moving Average
    sma = ta.SMA(df, timeperiod=30)
    
    #T3 - Triple Exponential Moving Average (T3)
    t3 = ta.T3(df, timeperiod=5, vfactor=0)
    
    #TEMA - Triple Exponential Moving Average
    tema = ta.TEMA(df, timeperiod=30)
    
    #TRIMA - Triangular Moving Average
    trima = ta.TRIMA(df, timeperiod=30)
    
    #WMA - Weighted Moving Average
    wma = ta.WMA(df, timeperiod=30)
    
    fig = plt.figure(figsize=(10,10))
    ax = fig.add_subplot(1,1,1)
    ax.xaxis.set_major_locator(ticker.MaxNLocator(20))
    
    ax.set_xlabel('date')
    mpl_finance.candlestick2_ohlc \
    (ax, df['open'][:1000], df['high'][:1000], df['low'][:1000], df['close'][:1000], \
     width=0.5, colorup='r', colordown='b')
    
    ax.plot(df['date'], bb, label='bb')
    ax.plot(df['date'], dema, label='dema')
    ax.plot(df['date'], ema, label='ema')
    ax.plot(df['date'], ht, label='ht')
    ax.plot(df['date'], kama, label='kama')
    ax.plot(df['date'], ma, label='ma')
    ax.plot(df['date'], mpt, label='mpt')
    ax.plot(df['date'], mpr, label='mpr')
    #ax.plot(df['date'], sar, label='sar')
    #ax.plot(df['date'], sarext, label='sarext')
    ax.plot(df['date'], sma, label='sma')
    ax.plot(df['date'], t3, label='t3')
    ax.plot(df['date'], tema, label='tema')
    ax.plot(df['date'], trima, label='trima')
    ax.plot(df['date'], wma, label='wma')

    ax.legend(loc=5)
    plt.grid()
    plt.show()