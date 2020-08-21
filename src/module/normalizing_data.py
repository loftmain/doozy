# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 16:49:44 2020

@author: giho9
"""

class Normalization:
    '''

    20200819 126~149 LINE 옵션 입력할 때 대문자만 입력가능하게 변경

    지표데이터를 정규화 한다.
    
    정규화 종류
    
    - 변화율을 나타내는 rate
    
    - LOG와 EXP 함수를 이용한 옵션이 존재
    
    - 사용자가 원하는 정규화식을 직접 입력할 수도 있다.
    
    - 한 번에 여러개의 정규화도 가능하다.
    
    - 단일 정규화데이터 생성은 USER, 복수개의 정규화 데이터 생성은 USERS이다.
    
    사용 예시
    ----------
    
    >>> folder = os.listdir('independent')
    # 작업 경로의 independent 폴더 안에 파일 리스트를 가져온다
    
    >>> index_list = [file.split('.')[0] for file in folder]
    # 파일 리스트에서 .csv 삭제하고 지표 이름만 남긴 리스트를 생성한다,
    
    >>> index_df_list = [pd.read_csv('independent/'+file) for file in folder]
    # 폴더 안의 모든 경제지표 csv파일을 읽어서 데이터프레임에 각각 저장한다.
     
    >>> moon = 'df[tag] * 100'
    
    - 사용자 정의 정규화식을 입력한다. 위는 단순히 데이터에 100을 곱한 것이다.
    - 데이터는 df[tag]라는 이름으로 통일한다.
    - 만약 복수개의 정규화데이터를 생성하고 싶다면 set_option의 파라미터를
      USERS로 하고, df['나만의정규화데이터'] = df[tag] * 100 - 1과 같이
      equal까지 모두 기입한다. 여러줄을 입력하여도 상관없다. 파이썬 스타일 문법
      이라면 모두 적용된다.
    
    >>> mod = Normalization()
    # 클래스 선언
    
    >>> mod.set_option(index_df_list, index_list, 'test', 'USER', moon)
    # 옵션 세팅
    
    # mod.scaling()
    # 실행
    
    
    '''
    def set_option(self, dilist, ilist, fname, nopt, exe):
        '''
        

        Parameters
        ----------
        dilist : list
            정규화할 경제지표 데이터프레임들이 들어있는 리스트
            
        ilist : list
            정규화할 경제지표 이름들이 들어있는 리스트
            
        fname : str
            정규화된 경제지표들을 넣을 폴더 이름
            
        nopt : str
            정규화 옵션
            
        exe : str
            사용자 정의 정규화식을 사용할 때 사용

        Returns
        -------
        None

        '''
        
        self._dilist = dilist
        self._ilist = ilist
        self._fname = fname
        self._nopt = nopt
        self._exe = exe
        
    def inspect_index_folder(self, path):
        '''
        
        경제지표 파일들을 저장할 폴더를 만드는 함수이다.
        
        폴더가 이미 존재한다면 생성하지 않고, 존재하지 않는다면 생성한다.
        
        self : object
        
        self._fname : str
        
                정규화된 경제지표들을 넣을 폴더이름

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

    def select_option(self, df, tag):

        import numpy as np

        if self._nopt == 'RATE':
            df[tag + 'rate'] = (df[tag] / df[tag].shift(+1)) - 1

        if self._nopt == 'LOGEXP':
            df[tag + 'rate'] = (df[tag] / df[tag].shift(+1))
            df[tag + 'EXP'] = np.exp(np.array(df[tag], dtype=np.float))
            df[tag + 'rate' + 'EXP'] = np.exp(np.array(df[tag + 'rate'], dtype=np.float))
            df[tag + 'LOG'] = np.log(np.array(df[tag], dtype=np.float))
            df[tag + 'rate' + 'LOG'] = np.log(np.array(df[tag + 'rate'], dtype=np.float))
            df[tag + 'logexp'] = df[tag + 'rate' + 'LOG'] * 100 - df[tag + 'rate' + 'EXP']

            del df[tag + 'rate']
            del df[tag + 'EXP']
            del df[tag + 'rate' + 'EXP']
            del df[tag + 'LOG']
            del df[tag + 'rate' + 'LOG']

        if self._nopt == 'USER':
            df[tag + 'user'] = eval(self._exe)

        if self._nopt == 'USERS':
            exec(self._exe)

        return df

    def scaling(self, path):
        '''
        
        지표데이터를 정규화하는 함수

        Returns
        -------
        None.

        '''
        
        import os
        
        gpath = self.inspect_index_folder(path)
        
        for indi, index in zip(self._dilist, self._ilist):
            
            try:
                data = self.select_option(indi, index)
                print(index,': success')
            
                data.to_csv(os.path.join
                            (gpath, index) + '.csv', index=False) 
            except:
                print(index,': error(The bad data exists)')