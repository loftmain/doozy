# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 14:42:59 2020

@author: giho9
"""


class Gathering_target:
    '''
    
    DataReader를 사용하여 지수데이터들을 데이터프레임으로 받은 뒤,
    csv 파일로 만든다.
    
    만들어진 지수데이터 csv 파일은 사용자가 지정한
    이름으로 된 폴더안에 존재한다.
    
    사용 예시
    ----------
    
    >>> index_code = '^DJI'
    # Yahoo finance 다우존스 코드명
    
    pandas datareader와 finance datareader 코드명은 다를 수 있음
    
    example
        
    - ^DJI : DOW JONES (pandas datareader)
    - DJI : DOW JONES (finance datareader)
    
    >>> folder_name = 'test'
    # 만들어질 폴더 이름
    
    >>> starting_point = '2000-01-01'
    # 지수데이터 시작 날짜
    
    >>> dopt = 'PDR'
    # pandas datareader 사용시에 옵션명은 PDR
    # finance datareader 사용시에 옵션명은 FDR
    
    >>> mod = Gathering_target()
    # 클래스 선언
    
    >>> mod.set_option(index_code, folder_name, starting_point, dopt)
    # 옵션설정
    
    >>> mod.gathering()
    # 지수데이터 받아오기
    '''

    def set_option(self, code, fname, spoint, opt):
        '''
        
        클래스 멤버변수를 설정하는 함수이다.

        Parameters
        ----------
        code : str
        
            받아올 지수데이터 코드명
            
            예 :
                
                - ^DJI : DOW JONES(pandas datareader)
                - DJI : DOW JONES(finance datareader)
                - ^IXIC : NASDAQ(pandas datareader)
                - ^GSPC : S&P 500(pandas datareader)
                - KS11 : KOSPI(pandas datareader)
            
        fname : str
        
            지수데이터가 들어갈 폴더이름
            
        spoint : str
        
            지수데이터의 시작 날짜
            예 : '2000-01-01'
            
        opt : str
        
            PDR : pandas datareader에서 지수데이터 받아오기
            
            FDR : finance datareader에서 지수데이터 받아오기

        Returns
        -------
        None

        '''

        self._code = code
        self._fname = fname
        self._spoint = spoint
        self._opt = opt

    def inspect_index_folder(self, path):
        '''
        
        지수데이터 파일을 저장할 폴더를 만드는 함수이다.
        
        폴더가 이미 존재한다면 생성하지 않고, 존재하지 않는다면 생성한다.
        
        self : object
        
        self._fname : str
        
                지수데이터를 넣을 폴더이름

        Returns
        -------
        folderpath : str
        
            입력받은 폴더명으로 만들어진 폴더경로를 반환한다.

        '''
        import os
        if not os.path.exists(os.path.join(path, self._fname)):
            os.mkdir(os.path.join(path, self._fname))

        folderpath = \
            os.path.join(path, self._fname)
        return folderpath

    def preprocessing(self, origin):
        '''
        
        datareader에서 받아온 지수데이터 데이터프레임을 전처리하는 함수이다.
        
        어떤 전처리를 하는가?
        
        - 일간 데이터 -> 월간 데이터 변환
        - 중복행 제거
        - 이후 3개월의 Nan row 추가

        Parameters
        ----------
        origin : dataframe
            
            datareader에서 받아온 지수데이터 데이터프레임 원본

        Returns
        -------
        origin : dataframe
        
            전처리가 완료된 지수데이터 데이터프레임

        '''

        from dateutil.relativedelta import relativedelta

        origin = origin.resample('MS').first()
        origin = origin.reset_index()
        origin.drop_duplicates(["Date"], keep='last', inplace=True)

        for n in range(1, 4):
            origin.loc[len(origin), 'Date'] = \
                origin['Date'][len(origin) - n] + relativedelta(months=n)

        return origin

    def gathering(self, path):
        '''
        
        pandas datareader or finance datareader로 
        지수데이터를 받아, csv file에 저장하는 함수
        
        Parameters
        ----------
        
        self : object
        
        Returns
        -------
        None

        '''

        import os

        gpath = self.inspect_index_folder(path)

        if self._opt == 'PDR':

            import pandas_datareader.data as web

            try:
                df = web.DataReader(self._code, 'yahoo', self._spoint)
            except:
                print(self._code,
                      ': 이름이 잘못되었거나 접속이 지연되고 있습니다')
                pass

            df = self.preprocessing(df)

            df.to_csv(os.path.join
                      (gpath, self._code) + '.csv', index=False)

            print(self._code, ': 성공')

        if self._opt == 'FDR':

            import FinanceDataReader as fdr

            try:
                df = fdr.DataReader(self._code, self._spoint)
            except:
                print(self._code,
                      ': 이름이 잘못되었거나 접속이 지연되고 있습니다')
                pass

            df = self.preprocessing(df)

            df.to_csv(os.path.join
                      (gpath, self._code) + '.csv', index=False)

            print(self._code, ': 성공')
