# -*- coding: utf-8 -*-
"""
Created on Mon Dec 30 14:52:29 2019

@author: giho9
"""

class Marking:
    '''
    
    사용자로부터 종목데이터나 지수데이터를 입력받아 조건에 맞는 label을 생성한다. 
    label은 모델 학습에 사용되는 정답데이터이다. 예를 들면, 
    한 달 간의 주가상승률이 3% 이상인 달에 대해서 1과 0으로 마킹할 수 있다. 
    반대로 주가하락률이 3% 이상인 달에 대해서도 1과 0으로 마킹할 수 있다. 
    어떤 데이터에 대해서 마킹을 할 것인지는 사용자가 지정한 옵션에 따라 다르다. 
    월간 데이터와 일간 데이터를 선택할 수 있다. 
    월간 전략과 일간 전략이 구분되어 있다.
    
    사용 예시
    ----------
    
    >>> df = pd.read_csv('../path/^DJI.csv')
    # 다우존스 지수파일을 데이터프레임에 읽어옴
    
    >>> mod = Marking()
    # 클래스 선언

    >>> mod.set_option(df, ['0', '0',  '0.04'], ['High', 'Open', 'HM4UP'], 'up')
    # 옵션 설정
    # 위 옵션을 해석하자면 다음과 같다.
    # 시가 대비 고가가 4%이상 상승한 달에 대하여 레이블을 생성하고
      컬럼명은 HM4UP으로 한다.
    
    >>> res = mod.create_label()
    # 데이터프레임에 레이블 생성
    
    '''
    def set_option(self, df, x_opt, y_opt, z_opt):
        '''
        

        Parameters
        ----------
        df : 데이터프레임
            읽어온 지수데이터 데이터프레임
            
        x_opt : list
            사이즈가 3인 리스트 안에 마킹 옵션이 들어있다.
            
            example : 
                [0, 0, 0.04] -> 1,2 번째 인자가 0, 0 이면 같은 달 안에서
                시가와 고가를 비교, 시가와 저가를 비교하는 것과 같이 행에서
                연산을 할 때의 인덱스 기준.
                월간 4%상승이나 4% 하락 등을 나타낸다.
                
        y_opt : list
            사이즈가 3인 리스트 안에 마킹 옵션이 들어있다.
            
            example :
                ['High', 'Open', 'HM4UP'] -> 1,2 번째 인자는 연산을 할 데이터를
                나타낸다. 첫 번째가 고가이고 두번째가 시가라면 시가 대비 고가를
                의미한다. 
            
        z_opt : str
            n% 상승인지 하락인지에 대한 옵션
            up은 상승이고 down은 하락이다.
            
        

        Returns
        -------
        None.

        '''
        self._df = df
        self._x_opt = x_opt
        self._y_opt = y_opt
        self._z_opt = z_opt

    def _is_string(ele):
        '''
        
        문자열인지 검사하는 함수

        Parameters
        ----------
        ele : all object
            검사되어질 대상, 데이터 종류는 어떤 것도 들어올 가능성이 있다.

        Returns
        -------
        bool
            문자열이 맞으면 True, 아니면 False 반환

        '''
        try:
            str(ele)
            return True
        except ValueError:
            return False
        
    def _is_number(ele):
        '''
        
        숫자인지 검사하는 함수
        

        Parameters
        ----------
        ele : all object
            검사되어질 대상, 데이터 종류는 어떤 것도 들어올 가능성이 있다.

        Returns
        -------
        bool
            숫자가 맞으면 True, 아니면 False 반환

        '''
        try:
            float(ele)
            return True
        except ValueError:
            return False
        
    def check_option(self):
        '''
        
        입력 옵션이 정확한지 확인하는 함수
        
        Parameters
        ----------
        self : object
        
        Returns
        -------
        bool
            모든 옵션이 조건에 맞다면 True, 아니면 False 반환

        '''
        for x, y in zip(self._x_opt,self._y_opt):
            if not Marking._is_number(x) or not Marking._is_string(y):
                return False
        return True    
    
    def create_label(self):
        '''
        
        옵션에 맞는 레이블을 생성하는 함수

        Parameters
        ----------
        self : object

        Returns
        -------
        df : dataframe
            레이블이 생성된 데이터프레임을 반환

        '''
        
        import numpy as np
        
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