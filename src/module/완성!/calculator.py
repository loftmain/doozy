# -*- coding: utf-8 -*-
"""
Created on Wed Jul 15 16:58:46 2020

@author: giho9
"""

class Calculator:
    '''
    거래내역을 입력받아서 주간 수익률, 월간 수익률, 연간 수익률을 계산한다.
    
    
    사용 예시
    ----------
    
    >>> import pandas as pd
    >>> import pathlib
    >>> import json
    >>> import os
    
    >>> file = pathlib.Path(os.getcwd()+'\\TradingLog.json')
    >>> text = file.read_text(encoding='utf-8')
    >>> js = json.loads(text)
    >>> trade = pd.DataFrame(js)
    # json 거래내역 파일을 읽어와서 데이터프레임에 저장
    
    >>> mod = Calculator()
    # 클래스 선언
    
    >>> mod.insert_log(trade)
    # 거래내역 삽입
    
    >>> mod.create_dates()
    >>> mod.create_weeks()
    >>> mod.create_months()
    >>> mod.create_years()
    # 거래내역 날짜를 기반으로 날짜 생성

    >>> mod.calculation('week')
    >>> mod.calculation('month')
    >>> mod.calculation('year')
    # 주간 수익률, 월간 수익률, 연간 수익률 계산
    
    >>> mod.write_atlog('', 'week')
    >>> mod.write_atlog('', 'month')
    >>> mod.write_atlog('', 'year')
    # 주간 수익률, 월간 수익률, 연간 수익률 json파일 출력
    
    '''
    
    def __init__(self):
        
        '''
        클래스 멤버변수를 초기화하는 init 함수이다.
        
        
            Parameters
            ----------
    
            Returns
            -------
            None.
            
    
        '''
        import pandas as pd
        
        self._wast_log = pd.DataFrame(columns=
                                     ['datetime', 
                                      'asset', 
                                      'cumulative'])
        
        self._mast_log = pd.DataFrame(columns=
                                     ['datetime', 
                                      'asset', 
                                      'cumulative'])
        
        self._yast_log = pd.DataFrame(columns=
                                     ['datetime', 
                                      'asset', 
                                      'cumulative'])
        
        self._last_log = pd.DataFrame(columns=
                                     ['datetime', 
                                      'asset', 
                                      'cumulative'])
        
        self._weeks = list()
        self._months = list()
        self._years = list()
        self._endate = list()
        
    def insert_log(self, log):
        
        '''
        거래내역을 입력하는 함수이다.
        
            Parameters
            ----------
            log : DataFrame
                거래내역이 들어있는 데이터프레임
    
            Returns
            -------
            None.
        '''
        
        self._trd_log = log
    
    def create_dates(self):
        
        '''
            거래 시작 날짜와 마지막 날짜 사이의 모든 날짜를 구한다.
            
            Parameters
            ----------
            None.
            
            Returns
            -------
            None.
        
        '''
        
        
        import pandas as pd
        
        fod = self._trd_log['order_datetime'][0]
        lod = self._trd_log['order_datetime'][len(self._trd_log)-1]
        di = pd.date_range(start=fod, end=lod)
        dl = di.strftime("%Y-%m-%d").tolist()
        
        self._dates = dl
    
    def create_weeks(self):
        
        '''
            거래 시작 날짜와 마지막 날짜 사이의 모든 날짜에서
            금요일인 날짜만 남긴다.
            
            Parameters
            ----------
            None.
            
            Returns
            -------
            None.
        
        '''
        
        import datetime
        
        for date in self._dates:
            wtmp = datetime.datetime.strptime(date, "%Y-%m-%d")
            if wtmp.weekday() == 4: self._weeks.append(date)
            
    def create_months(self):
        
        '''
            거래 시작 날짜와 마지막 날짜 사이의 모든 날짜에서
            월 마지막인 날짜만 남긴다.
            ex) 
            
            Parameters
            ----------
            None.
            
            Returns
            -------
            None.
        
        '''
        import calendar
        
        for date in self._dates:
            y,m = str(date[0:4]), str(date[5:7])
            d = str(calendar.monthrange(int(date[0:4]), int(date[5:7]))[1])
            self._months.append(y + '-' + m + '-' + d)
        self._months = sorted(list(set(self._months)))
    
    def create_years(self):
        
        '''
            거래 시작 날짜와 마지막 날짜 사이의 모든 날짜에서
            연 마지막일 날짜만 남긴다.
            
            Parameters
            ----------
            None.
            
            Returns
            -------
            None.
        '''
        
        for date in self._dates:
            y = str(date[0:4]) + '-12-31'
            self._years.append(y)

        self._years = sorted(list(set(self._years)))
    
    def create_endate(self):
        '''
            마지막 날짜만 남긴다.
            
            Parameters
            ----------
            None.
            
            Returns
            -------
            None.
        '''
        
        self._endate.append(self._dates[-1])
    
    def rated(self, rdf, rdt):
        
        '''
            
        해당 시점 이전의 거래내역에 대해서 수익률을 계산한다.
        
        Parameters
        ----------
        rdf : DataFrame
            해당 시점 이전의 거래내역이 담긴 데이터프레임
        
        rdt : str
            주간 수익률인지, 월간 수익률인지, 연간 수익률인지

        Returns
        -------
        None.

        '''
        
        import FinanceDataReader as fdr
        import datetime
        import time
        
        t = rdt
        
        ist = list()
        
        if rdf.empty:
            
            return
        
        for _, pr in rdf.iterrows():
            
            pdf = fdr.DataReader(pr.item_code, rdt, rdt)
            
            while pdf.empty:
                
                rdt = str(datetime.datetime.strptime \
                    (rdt, '%Y-%m-%d') - datetime.timedelta(1))[:10]
                
                pdf = fdr.DataReader(pr.item_code, rdt, rdt)
                
                time.sleep(1)
                
                print(rdt)
                
            ist.append(int(pr['hold']) * int(pdf['Close']))

        ast = sum(ist) + int(rdf.tail(1)['res_cash'])
        
        cum = round(
            (ast) / (int(self._trd_log.head(1).order_value + \
                         self._trd_log.head(1).res_cash))
            ,3)
        
        atlog = {'datetime' : t, 
                'asset' : ast, 
                'cumulative' : cum}
        
        return atlog

    def calculation(self, opt):
        
        '''
        Parameters
        ----------
        opt : str
        
            주간 수익률 -> week
            월간 수익률 -> month
            연간 수익률 -> year
            
        Returns
        -------
        None.
        '''
        
        
        if opt == 'week': dates = self._weeks
        if opt == 'month': dates = self._months
        if opt == 'year': dates = self._years
        if opt =='all': dates = self._endate
        
        for dt in dates:
 
            tdf = self._trd_log.query("order_datetime < '%s'"%dt).\
                drop_duplicates(['item_code'], keep='last')
            
            log = self.rated(tdf, dt)
        
            if opt == 'week':
                self._wast_log = \
                    self._wast_log.append(log, ignore_index='True')
                print(self._wast_log)
            if opt == 'month':
                self._mast_log = \
                    self._mast_log.append(log, ignore_index='True')
                print(self._mast_log)
            if opt == 'year':
                self._yast_log = \
                    self._yast_log.append(log, ignore_index='True')
                print(self._yast_log)
            if opt == 'all':
                self._last_log = \
                    self._last_log.append(log, ignore_index='True')
                print(self._last_log)
                
                
    def write_atlog(self, apath, nopt):
        
        '''
        Parameters
        ----------
        apath : str
            파일을 저장할 경로
            
        nopt : str
            주간 수익률 -> week
            월간 수익률 -> month
            연간 수익률 -> year
            
        Returns
        -------
        None
        
        '''
        
        import json
        
        if nopt == 'week': adict = self._wast_log.to_dict(orient='record')
        if nopt == 'month': adict = self._mast_log.to_dict(orient='record')
        if nopt == 'year': adict = self._yast_log.to_dict(orient='record')
        if nopt == 'all': adict = self._last_log.to_dict(orient='record')
        
        #json.dumps(tdict, ensure_ascii=False, indent='\t')
        with open(apath+'Asset'+nopt+'.json', 'w+', encoding='utf-8') as make_file:
            json.dump(adict, make_file, ensure_ascii=False, indent='\t')
            
if __name__ == '__main__':
    
    import pandas as pd
    import pathlib
    import json
    import os
    
    file = pathlib.Path(os.getcwd()+'\\TradingLog.json')
    text = file.read_text(encoding='utf-8')
    js = json.loads(text)
    trade = pd.DataFrame(js)
    
    mod = Calculator()
    
    mod.insert_log(trade)
    
    mod.create_dates()
    mod.create_weeks()
    mod.create_months()
    mod.create_years()
    mod.create_endate()
    
    #mod.calculation('week')
    #mod.calculation('month')
    #mod.calculation('year')
    #mod.calculation('all')
    
    #mod.write_atlog('', 'week')
    #mod.write_atlog('', 'month')
    #mod.write_atlog('', 'year')