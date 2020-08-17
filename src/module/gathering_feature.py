# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 17:24:07 2020

@author: giho9
"""

class Gathering_Feature:
    '''
    
    fredapi를 사용하여 경제지표들을 데이터프레임으로 받은 뒤,
    개별 csv파일들로 만든다.
    
    만들어진 경제지표 csv 파일들은 사용자가 지정한
    이름으로 된 폴더안에 모두 존재한다.
    
    사용 예시
    ----------
    다운받을 경제지표 목록을 list로 작성, FRED에서 지정한 약어를 넣어주면 된다.
    
    >>> index_list = ['BAA', 'HOUST', 'NEWORDER']
    # 무디스채권수익률, 미국신규주택착공, 미국핵심자본재신규주문
    
    >>> folder_name = 'test'
    # 만들어질 폴더 이름
    
    >>> starting_point = '2000-01-01'
    # 경제지표 시작 날짜, 2000년 1월 1일 데이터부터 가져오겠다는 의미

    >>> private_key = '3b2795f81c94f1a105d1e4fc3661a45e'
    # fredapi를 사용하기 위해 발급받은 개인키
    
    >>> mod = Gathering_Feature()
    # 클래스 선언

    >>> mod.set_option(index_list, folder_name, starting_point, private_key)
    # 옵션설정
    
    >>> mod.gathering()
    경제지표 받아오기
    
    '''
    
    def set_option(self, features, fname, spoint, key):
        '''
        클래스 멤버변수를 설정하는 함수이다.
        
        Parameters
        ----------
        features : list
        
            받아올 경제지표 목록
            예 : ['BAA', 'HOUST', 'NEWORDER']
            
        fname : str
        
            경제지표가 들어갈 폴더이름
            
        spoint : str
        
            경제지표의 시작 날짜
            예 : '2000-01-01'
            
        key : str
        
            Fredapi를 사용하기 위해서 발급받은 개인키

        Returns
        -------
        None

        '''
        self._features = features
        self._key = key
        self._fname = fname
        self._spoint = spoint
    
    def inspect_index_folder(self, path):
        '''
        경제지표 파일들을 저장할 폴더를 만드는 함수이다.
        
        폴더가 이미 존재한다면 생성하지 않고, 존재하지 않는다면 생성한다.
        
        self : object
        
        self._fname : str
        
                경제지표를 넣을 폴더이름

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
    
    def preprocessing(self, origin, ind):
        '''
        Fredapi에서 받아온 경제지표 데이터프레임을 전처리하는 함수이다.
        
        어떤 전처리를 하는가?
        
        - 중복행 제거
        - 시작날짜 이전의 날짜들 삭제
        - column rename
        - column name sort
        - index 재설정
        - 이후 3개월의 Nan row 추가

        Parameters
        ----------
        self : object
        
        self._spoint : str
        
            경제지표 시작 날짜
        
        origin : dataframe
        
            fredapi에서 받아온 경제지표 데이터프레임 원본
            
        ind : str
            
            경제지표 약어
            
            예 : 무디스채권수익률 -> 'BAA'

        Returns
        -------
        origin : dataframe
        
            전처리가 완료된 경제지표 데이터프레임

        '''
        import pandas as pd
        from datetime import datetime
        from dateutil.relativedelta import relativedelta
        
        tp = datetime.strptime('2000-01-01', '%Y-%m-%d').date()
        origin.drop_duplicates(["date"], keep='last', inplace=True)
        origin['Date'] = origin['date'].dt.date
        origin.rename(columns={'value':ind}, inplace=True)
        origin = origin[['Date', ind]]
        origin.drop(origin[origin.Date < tp].index, inplace=True)
        origin.index = pd.RangeIndex(len(origin.index))
        
        for n in range(1,4):
            origin.loc[len(origin), 'Date'] = \
            origin['Date'][len(origin) - n] + relativedelta(months=n)
        
        return origin
        
    def gathering(self, path):
        '''
        fred로부터 경제지표 데이터를 받아, csv file에 개별 저장하는 함수
        
        self : object

        Returns
        -------
        None

        '''
        
        from fredapi import Fred
        import os
        
        gpath = self.inspect_index_folder(path)

        pkey = Fred(api_key=self._key)

        for index in self._features:
            
            try:
                data = pkey.get_series_all_releases(index)
            except:
                print(index, ': 이름이 잘못되었거나 접속이 지연되고 있습니다')
                continue
            
            data = self.preprocessing(data, index)
            
            data.to_csv(os.path.join
                      (gpath, index) + '.csv', index=False)
            print(index, ': 성공')