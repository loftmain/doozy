# -*- coding: utf-8 -*-
"""
Created on Wed Jul 15 16:58:46 2020

@author: giho9
"""

class Simulator:

    '''
    주문서를 입력받으면 과거데이터를 이용하여 수익률 시뮬레이션을 수행한다.
    주식종목, ETF, 가상화폐(미구현)에 대해서 시뮬레이션이 가능하다.
    
    사용 예시
    ----------


    >>> file = pathlib.Path(os.getcwd()+'\\order.json')
    >>> text = file.read_text(encoding='utf-8')
    >>> js = json.loads(text)
    >>> order = pd.DataFrame(js)
    # 주문서를 json file에서 읽어온 뒤 데이터프레임에 저장한다.
    
    order type
    
        buy : 매수
        
        sell : 매도
        
    (buy) order_option
    
        all : 보유현금 기준 최대매수
        
        por : 보유자산의 일정 퍼센트만큼 매수
        
        cash : 지정금액 이하 최대매수
        
        scnt : 보유주식의 일정 주식수 매수
        
    (buy) order_value
    
        all : 0이든 비워놓든 상관없다.
        
        por : 0.5, 0,7과 같이 비율로 설정
        
        cash : 5000000, 1000000과 같이 금액으로 설정
        
        scnt : 100, 500과 같이 매수할 주식 수를 입력
        
    (sell) order_option
    
        all : 보유종목 전량매도
        
        por : 보유주식의 일정 퍼센트만큼 매도
        
        scnt : 보유주식의 일정 주식수 매도
        
    (sell) order_value
    
        all : 0이든 비워놓든 상관없다.
        
        por : 0.5, 0.7과 같이 비율로 설정
        
        scnt : 100, 500과 같이 매도할 주식 수를 입력
    
    example) order.json
    
    [
    	{
    		"order_datetime": "2018-04-27",
    		"order_type": "buy",
    		"item_code": "032640",
    		"item_name": "LG유플러스",
    		"order_price": "12300",
    		"order_option": "cash",
    		"order_value": "5000000"
    	},
        {
    		"order_datetime": "2018-04-27",
    		"order_type": "sell",
    		"item_code": "032640",
    		"item_name": "LG유플러스",
    		"order_price": "12300",
    		"order_option": "scnt",
    		"order_value": "150"
    	}  
    ]
    
    
    >>> file = pathlib.Path(os.getcwd()+'\\status.json')
    >>> text = file.read_text(encoding='utf-8')
    >>> status = json.loads(text)
    # 보유현금과 보유종목들이 들어있는 Status.json을 사용할 수 있다.
    # Status.json이 없이 초기자본 세팅만으로도 시뮬레이션 진행이 가능하다.
    
    example) status.json
    
    {
    	"cash": 5465000,
    	"stock": [
    		{
    			"item_name": "LG유플러스",
    			"item_code": "032640",
    			"item_count": 200,
    			"avg_price": 13571
    		},
    		{
    			"item_name": "SK하이닉스",
    			"item_code": "000660",
    			"item_count": 200,
    			"avg_price": 84000
    		},
    		{
    			"item_name": "엔씨소프트",
    			"item_code": "036570",
    			"item_count": 100,
    			"avg_price": 400000
    		},
    		{
    			"item_name": "POSCO",
    			"item_code": "005490",
    			"item_count": 200,
    			"avg_price": 245000
    		},
    		{
    			"item_name": "아모레퍼시픽",
    			"item_code": "090430",
    			"item_count": 300,
    			"avg_price": 173000
    		},
    		{
    			"item_name": "셀트리온",
    			"item_code": "068270",
    			"item_count": 200,
    			"avg_price": 210000
    		}
    	]
    }
    
    
    >>> mod = Simulator()
    # 시뮬레이터 클래스 생성
    
    >>> mod.insert_order(order)
    # 주문서 삽입
    
    >>> mod.set_cash(10000000)
    # 초기자본세팅
    
    >>> mod.simulation()
    # 주문서로 시뮬레이션 실행
    # 시뮬레이션이 끝난 후 멤버변수인 _trd_log와 _stu_log에 기록이 담겨있다.
    
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
        
        self._trd_log = pd.DataFrame(columns=
                                     ['order_datetime', 
                                      'order_type', 
                                      'item_code', 
                                      'item_name', 
                                      'order_value',
                                      'order_count',
                                      'price', 
                                      'avg_price', 
                                      'res_cash', 
                                      'hold'])
        
        self._stu_log = pd.DataFrame(columns=
                                     ['item_code',
                                      'item_name',
                                      'item_count',
                                      'avg_price'])
        
        self._cash = 0
        
    def insert_order(self, odf):
        
        '''
        주문서를 입력하는 함수이다.
        
            Parameters
            ----------
            odf : DataFrame
                주문내역이 들어있는 데이터프레임
    
            Returns
            -------
            None.
        '''
        
        self._order_sheet = odf

    def set_status(self, sdf):
        
        import pandas as pd
        
        '''
        보유금액과 보유종목을 입력할 수 있는 함수이다.
        특정 시뮬레이션을 수행하고 상태를 이어서 진행하고 싶을 때 사용
        
        
            Parameters
            ----------
            sdf : DataFrame
                보유금액과 보유종목이 들어있는 데이터프레임
    
            Returns
            -------
            None.
            
    
        '''
        
        self._cash = sdf['cash']
        self._stu_log = pd.DataFrame(sdf['stock'])
    
    def set_cash(self, cv):
        
        '''
        초기자본금 설정을 위한 함수이다.
        
        
            Parameters
            ----------
            cv : int
                초기자본금
    
            Returns
            -------
            None.
            
    
        '''
        
        self._cash = cv
        
    def get_price(self, pr):
        
        '''
        finance datareader를 이용하여 가격정보를 가져오는 함수이다.
        
        
            Parameters
            ----------
            pr : DataFrame(row)
                특정날짜의 주문내역.
                루프가 진행중인 데이터프레임의 한 '행'이다.
    
            Returns
            -------
            Price : boolean or int
                가격정보가 존재하지 않는다면 False를 반환
        '''
        
        import FinanceDataReader as fdr
        
        try:
            pdf = fdr.DataReader(
                pr.item_code, pr.order_datetime, pr.order_datetime)
        except:
            self.print_error(4)
        
        if len(pdf) == 0:
            self.print_error(4)
            return False
        
        ran = int(pr.order_price)*0.01
        
        if not int(pdf['High'])+ran > int(pr.order_price) > int(pdf['Low'])-ran:
            self.print_error(3)
            return False
        
        return int(pdf['Close'])
    
    def trade(self, tr):
        
        '''
        매수 or 매도에 따라 거래 실행
        
        
            Parameters
            ----------
            tr : DataFrame(row)
                특정날짜의 주문내역.
                루프가 진행중인 데이터프레임의 한 '행'이다.
    
            Returns
            -------
            None.
            
    
        '''
        
        if tr.order_type == 'buy': self.buy(tr)
            
        if tr.order_type == 'sell': self.sell(tr)
    
    def buying(self, byr, bvc, bvm):
        
        '''
        (매수)주문금액, (매수)주문량을 입력받고 주문결과를 로그에 기록한다.
        
        
            Parameters
            ----------
            byr : DataFrame(row)
            
                특정날짜의 주문내역.
                
                루프가 진행중인 데이터프레임의 한 '행'이다.
                
            bvc : int
            
                매수량
                
            bvm : int
            
                매수가격
    
            Returns
            -------
            None.
            
    
        '''
        
        if len(self._stu_log[self._stu_log['item_code']==byr.item_code]
                ['item_count']) != 0:
            
            itemvalue = \
                int(self._stu_log[self._stu_log['item_code']==byr.item_code]
                ['item_count']) + bvc

            avgprice = \
                (bvm + 
                 (self._stu_log[self._stu_log['item_code']==byr.item_code]
                  ['avg_price'] * \
                  self._stu_log[self._stu_log['item_code']==byr.item_code]
                  ['item_count'])) / int(itemvalue)
                
        else:
            itemvalue = bvc
            avgprice = int(byr.order_price)
        
        
        bslog = {'item_code' : byr.item_code,
                'item_name' : byr.item_name,
                'item_count' : int(itemvalue),
                'avg_price' : int(avgprice)}

        btlog = {'order_datetime' : byr.order_datetime, 
                'order_type' : byr.order_type, 
                'item_code' : byr.item_code, 
                'item_name' : byr.item_name, 
                'order_value' : bvm,
                'order_count' : bvc,
                'price' : int(byr.order_price),
                'avg_price' : int(avgprice),
                'res_cash' : int(self._cash - bvm),
                'hold' : int(itemvalue)}
        
        self._cash = int(self._cash - bvm)
        self._stu_log = self._stu_log.append(bslog, ignore_index='True').\
                        drop_duplicates(["item_code"], keep="last")
        self._trd_log = self._trd_log.append(btlog, ignore_index='True')
    
    def buy(self, br):
        
        '''
        매수 옵션에 따라 거래 진행
        
        
            Parameters
            ----------
            br : DataFrame(row)
                특정날짜의 주문내역.
                루프가 진행중인 데이터프레임의 한 '행'이다.
    
            Returns
            -------
            None.
            
    
        '''
        
        if br.order_option == 'all':
            
            if self._cash < int(br.order_price):
                self.print_error(1)
                return
            
            volcount = int(self._cash / int(br.order_price))
            volmoney = volcount * int(br.order_price)
            
            self.buying(br, volcount, volmoney)
        
        if br.order_option == 'por':
            
            polcash = self._cash * float(br.order_value)
            
            if polcash < int(br.order_price):
                self.print_error(1)
                return
            
            volcount = int(polcash / int(br.order_price))
            volmoney = int(volcount) * int(br.order_price)
            
            self.buying(br, volcount, volmoney)
            
        if br.order_option == 'cash':
            
            if self._cash < int(br.order_value) and \
                int(br.order_value) < int(br.order_price):
                self.print_error(1)
                return
                
            volcount = int(br.order_value) / int(br.order_price)
            volmoney = volcount * int(br.order_price)
            
            self.buying(br, volcount, volmoney)
            
        if br.order_option == 'scnt':
            
            if self._cash < int(br.order_price) * int(br.order_value):
                self.print_error(1)
                return
            
            volcount = int(br.order_value)
            volmoney = volcount * int(br.order_price)
            
            self.buying(br, volcount, volmoney)
        
    def selling(self, syr, svc, svm):

        '''
        (매도)주문금액, (매도)주문량을 입력받고 주문결과를 로그에 기록한다.
        
        
            Parameters
            ----------
            syr : DataFrame(row)
                특정날짜의 주문내역.
                루프가 진행중인 데이터프레임의 한 '행'이다.
            
            svc : int
                매도량
                
            svm :
                매도금액
            
            Returns
            -------
            None.
            
    
        '''
        itemvalue = int(self._stu_log[self._stu_log['item_code']==syr.item_code]
                ['item_count']) - svc
        
        avgprice = int(self._stu_log[self._stu_log['item_code']==syr.item_code]
                  ['avg_price'])
        
        sslog = {'item_code' : syr.item_code,
                'item_name' : syr.item_name,
                'item_count' : int(itemvalue),
                'avg_price' : int(avgprice)}

        stlog = {'order_datetime' : syr.order_datetime, 
                'order_type' : syr.order_type, 
                'item_code' : syr.item_code, 
                'item_name' : syr.item_name, 
                'order_value' : svm,
                'order_count' : svc,
                'price' : int(syr.order_price),
                'avg_price' : int(avgprice),
                'res_cash' : int(self._cash + svm),
                'hold' : int(itemvalue)}
        
        self._cash = int(self._cash + svm)
        self._stu_log = self._stu_log.append(sslog, ignore_index='True').\
                        drop_duplicates(["item_code"], keep="last")
        self._trd_log = self._trd_log.append(stlog, ignore_index='True')
        
    def sell(self, sr):
        
        '''
        매도 옵션에 따라 거래 진행
        
        
            Parameters
            ----------
            sr : DataFrame(row)
                특정날짜의 주문내역.
                루프가 진행중인 데이터프레임의 한 '행'이다.
    
            Returns
            -------
            None.
            
    
        '''
        
        if sr.order_option == 'all':
            
            if len(self._stu_log[self._stu_log['item_code']==sr.item_code] \
                ['item_count']) == 0:
                self.print_error(2)
                return
            
            volcount = \
                int(self._stu_log[self._stu_log['item_code']==sr.item_code] \
                ['item_count'])
            volmoney = volcount * int(sr.order_price)
            
            self.selling(sr, volcount, volmoney)
            
        if sr.order_option == 'por':
            
            if len(self._stu_log[self._stu_log['item_code']==sr.item_code] \
                ['item_count']) == 0:
                self.print_error(2)
                return
            
            volcount = \
                int(self._stu_log[self._stu_log['item_code']==sr.item_code] \
                ['item_count']) * float(sr.order_value)
            volmoney = volcount * int(sr.order_price)
            
            self.selling(sr, volcount, volmoney)
            
        if sr.order_option == 'scnt':
            
            if len(self._stu_log[self._stu_log['item_code']==sr.item_code] \
                ['item_count']) == 0 or \
                int(self._stu_log[self._stu_log['item_name']==sr.item_name]
                ['item_count']) < int(sr.order_value):
                self.print_error(2)
                return
            
            volcount = int(sr.order_value)
            volmoney = volcount * int(sr.order_price)
            
            self.selling(sr, volcount, volmoney)
        
    def write_trlog(self, tpath):
        
        '''
        Write TraingLog.json
        
        
            Parameters
            ----------
            wtlog : DataFrame(row)
                
                거래결과들이 담겨있는 데이터프레임
    
            Returns
            -------
            None.
            
    
        '''
        
        import json
        
        tdict = self._trd_log.to_dict(orient='record')
        #json.dumps(tdict, ensure_ascii=False, indent='\t')
        with open(tpath+'TradingLog.json', 'w+', encoding='utf-8') as make_file:
            json.dump(tdict, make_file, ensure_ascii=False, indent='\t')
    
    def write_stlog(self, spath):
        
        '''
        Write TraingLog.json
        
        
            Parameters
            ----------
            stlog : DataFrame(row)
                
                보유종목이 담겨있는 데이터프레임
    
            Returns
            -------
            None.
            
    
        '''
        
        import json
        
        sdict = self._stu_log.to_dict(orient='record')
        sdict = {'cash' : self._cash, 'stock' : sdict}
        #json.dumps(tdict, ensure_ascii=False, indent='\t')
        with open(spath+'Status.json', 'w+', encoding='utf-8') as make_file:
            json.dump(sdict, make_file, ensure_ascii=False, indent='\t')
        
    def simulation(self):
        
        '''
        수익률 시뮬레이션을 수행한다.
        
        
            Parameters
            ----------
            wtlog : DataFrame(row)
                
                거래결과들이 담겨있는 데이터프레임
    
            Returns
            -------
            None.
            
    
        '''
        
        for _, row in self._order_sheet.iterrows():
            
            price = self.get_price(row)
            
            if not price:
                continue
            
            self.trade(row)
            
            print(self._trd_log)
        
    def print_error(self, erc):
        '''
        
        Parameters
        ----------
        erc : TYPE
            DESCRIPTION.

        Returns
        -------
        None.
        
        error code 1 -> 최소현금이 부족하여 구매불가
        error code 2 -> 종목을 보유하지 않았거나 보유량이 부족하여 판매불가
        error code 3 -> 매수 or 매도 희망가격이 고가와 저가 사이가 아님
        error code 4 -> Finance Data로부터 데이터를 불러올 수 없음
        error code
        error code
        error code

        '''
        
        error = {1 : '최소현금이 부족하여 구매불가',
                 2 : '종목을 보유하지 않았거나 보유량이 부족하여 판매불가',
                 3 : '매수 or 매도 희망가격이 고가와 저가 사이가 아님',
                 4 : 'Finance Data로부터 데이터를 불러올 수 없음'}
        
        print('error code {} : {}'.format(erc, error[erc]))


if __name__ == '__main__':
    
    import pandas as pd
    import pathlib
    import json
    import os

    file = pathlib.Path(os.getcwd()+'/order.json')
    text = file.read_text(encoding='utf-8')
    js = json.loads(text)
    order = pd.DataFrame(js)
    
    #file = pathlib.Path(os.getcwd()+'\\statuslog.json')
    #text = file.read_text(encoding='utf-8')
    #status = json.loads(text)
    
    mod = Simulator()
    
    mod.insert_order(order)
    
    #mod.set_status(status)
    
    mod.set_cash(100000000)
    
    mod.simulation()
    
    mod.write_trlog('')
    
    mod.write_stlog('')
