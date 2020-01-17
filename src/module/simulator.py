import pandas as pd
import re
import pathlib
import json
import datetime
from datetime import timedelta
import pandas_datareader.data as web
from urllib.request import urlopen
from bs4 import BeautifulSoup

# =============================================================================
# def get_lastpage(url):
#     '''
#     naver에서 종목별 주가데이터는 한 페이지당 데이터가 10개씩 들어가있다.
#     마지막 페이지를 얻기 위한 함수이다.
#     
#     [입력]
#     -종목데이터가 존재하는 url
#     
#     [출력]
#     -마지막 페이지 숫자
#     
#     '''
#     
#     html = urlopen(url)
#     source = BeautifulSoup(html.read(), "html.parser")
#     navigation = source.find_all("table", align="center")
#     section = navigation[0].find_all("td", class_="pgRR")
#     
#     if not section:
#         page = 1
#         return page
# 
#     page = section[0].a.get('href')[-3:]
#     page = re.sub("[^0-9]", "", page)
#     page = int(page)
# 
#     return page
# 
# def get_url(code):
#     '''
#     종목 코드를 입력하면 해당 종목데이터가 있는 url을 알려주는 함수이다.
#     
#     [입력]
#     -종목 코드
#     
#     [출력]
#     -해당 종목데이터가 존재하는 url
#     
#     '''
#     #code = \
#     #code_df.query("name=='{}'".format(item_name))['code'].to_string(index=False)
#     
#     url = \
#     'http://finance.naver.com/item/sise_day.nhn?code={code}'.format(code=code)
#     url = url.replace(" ", "")
#     print("요청 URL = {}".format(url)) 
#     return url
# =============================================================================

def load_json(path):
    '''
    json file의 path를 입력받아서 데이터프레임으로 load하는 함수이다.
    
    [입력]
    -파일경로
    
    [출력]
    -데이터프레임
    
    '''
    file = pathlib.Path(path)
    text = file.read_text(encoding='utf-8')
    js = json.loads(text)
    df = pd.DataFrame(js)
    return df

def create_dataframe(column):
    '''
    데이터프레임을 생성한다. 생성시에 원하는 column을 지정할 수 있다.
    
    [입력]
    -데이터프레임의 column들이 담긴 list
    
    [출력]
    -데이터프레임
    '''
    df = pd.DataFrame(columns=column)
    return df

def get_price(row):
    '''
    날짜와 종목코드를 입력하면 가격을 알려주는 함수
    
    [입력]
    -데이터프레임 행(row)
    
    [출력]
    -해당 날짜의 수정종가
    '''
    start = \
    datetime.datetime.strptime(row.order_datetime, '%Y-%m-%d').date()
    try:
        df = \
        web.DataReader(row.itemcode+'.KS', 'yahoo', start, start+timedelta(days=1))
        df = df.reset_index()
    except(KeyError):
        return False
    
    pass
if __name__ == "__main__":
    capital = 10000000 # form에서 입력받음
    path = 'Order.json' # form에서 입력받
    order_sheet = load_json(path)

    return int(df['Adj Close'][0])

def trade_buy(row):
    pass
def trade_sell(row):ime', 'item_code', 'item_name', 'order_type',
              'vol_money', 'vol_colunt', 'price', 'avg_price', 'cash']
    s_column = ['item', 'item_code', 'item_count', 'avg_price']
    
    trading_log = create_dataframe(t_column)
    status_log = create_dataframe(s_column)
    
    for index, row in order_sheet.iterrows():

        price = get_price(row)
        
        if not price: 
            # fail log 작성
            continue
        
    