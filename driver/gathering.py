# -*- coding: utf-8 -*-
"""
Created on Thu Jan  2 11:29:32 2020

@author: giho9
"""

import pandas as pd
import os
import sys
from datetime import datetime
from dateutil.relativedelta import relativedelta
from pandas import ExcelWriter
from fredapi import Fred

fred = Fred(api_key='3b2795f81c94f1a105d1e4fc3661a45e')

class Gathering:
    
    def inspect_indicator(self, )