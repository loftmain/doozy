# -*- coding: utf-8 -*-
"""
Created on Mon Dec 30 14:52:29 2019

@author: giho9
"""

import numpy as np
import pandas as pd


class Marking:
    def set_option(self, df, x_opt, y_opt, z_opt):
        self._df = df
        self._x_opt = x_opt
        self._y_opt = y_opt
        self._z_opt = z_opt

    def _is_string(ele):
        try:
            str(ele)
            return True
        except ValueError:
            return False
        
    def _is_number(ele):
        try:
            float(ele)
            return True
        except ValueError:
            return False
        
    def check_option(self):
        for x, y in zip(self._x_opt,self._y_opt):
            if not Marking._is_number(x) or not Marking._is_string(y):
                return False
        return True    
    
    def create_label(self):
        
        if not Marking.check_option(self): return False
        
        if self._z_opt == 'up':
            self._df[self._y_opt[2]] = \
            np.where((
                    self._df[self._y_opt[0]].shift(float(self._x_opt[0]))/
                    self._df[self._y_opt[1]].shift(float(self._x_opt[1]))-1
                    >= float(self._x_opt[2])),1,0)
            
        elif self._z_opt == 'down':
            self._df[self._y_opt[2]] = \
            np.where((
                    self._df[self._y_opt[0]].shift(float(self._x_opt[0]))/
                    self._df[self._y_opt[1]].shift(float(self._x_opt[1]))-1
                    <= float(self._x_opt[2])),1,0)
        else:
            return False
        return self._df

if __name__ == '__main__':
    df = pd.read_csv('dependent/^DJI.csv')
    t = Marking()
    t.set_option(df, ['0', '0',  '0.04'], ['High', 'Open', 'HM4UP'], 'up')
    result = t.create_label()
    result.to_csv('test.csv', header=True, index=False, encoding='ms949')