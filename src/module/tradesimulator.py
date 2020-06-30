# -*- coding: utf-8 -*-
import os
# silence warnings
import warnings
from collections import OrderedDict

import pandas as pd
import pytz
import zipline
from trading_calendars import get_calendar
from zipline.api import order_percent, record, symbol, set_benchmark

from src.module.io import set_save_folder

warnings.filterwarnings('ignore')


def setup_panel(file_path, stock_name):
    """
    Zipline 에서 외부 데이터를 가져와서 사용하는 것은 가능하지만
    BUY/SELL 과 같은 SIGNAL 을 데이터에 넣는 것을 지원하지 않는다.
    이를 해결하기 위해  pandas 의 panel 을 사용하여 SIGNAL 을
    FAKE 주가 데이터로 인식시켜 Zipline 내부에서 사용할 수 있는
    Panel 을 return 한다.

    :param file_path: simulation 하는 order csv 파일 경로
    :param stock_name:
    :return: 판넬, 시작날짜, 끝 날짜
    """

    data = OrderedDict()
    data['originPrice'] = pd.read_csv(file_path, index_col=0, parse_dates=['Date'])
    data['originPrice'] = data['originPrice'][["Open", "High", "Low", "Close", "Volume"]]
    data['updown'] = pd.read_csv(file_path, index_col=0, parse_dates=['Date'])
    data['updown']['null1'] = 0
    data['updown']['null2'] = 0
    data['updown']['null3'] = 0
    data['updown'] = data['updown'][["null1", "null2", "null3", "buy", "sell"]]
    data['originPrice'].rename(columns={"Open": "open",
                                        "High": "high",
                                        "Low": "low",
                                        "Close": "close",
                                        "Volume": "volume"}, inplace=True)
    # FAKE 주가 데이터 <- BUY / SELL SIGNAL
    data['updown'].rename(columns={"null1": "open",
                                   "null2": "high",
                                   "null3": "low",
                                   "buy": "close",
                                   "sell": "volume"}, inplace=True)
    # TODO: Pandas의 Panel이 곧 삭제될 예정 -> 다른 것으로 변경해야함
    panel = pd.Panel(data)
    panel.minor_axis = ["open", "high", "low", "close", "volume"]
    panel.major_axis = panel.major_axis.tz_localize(pytz.utc)
    return panel, panel['originPrice'].index[0], panel['originPrice'].index[-1]
    # TODO: 여기서 오류 - 날짜 문제인듯


def set_calendar(cal):
    """
    Zipline 은 각 나라의 주가 Calendar 에 맞추어
    Backtesting 을 진행한다.
    따라서, trading_calendars API 를 사용하여
    사용자가 지정한 Calendar 에 맞추어
    Zipline 을 실행할 시에 적절한 Calendar를 넣어준다.

    현재 US와 KR 만 지원한다.
    :param cal: UI에서 입력된 값 ( US, KR )
    :return: Calendar-data
    """

    if cal == 'US':
        calendar = get_calendar('XNYS')
    elif cal == 'KR':
        calendar = get_calendar('XKRX')
    else:
        calendar = 'err'
    return calendar


def initialize(context):
    """
    Zipline 에서 기본적으로 사용되는 initialize 함수
    :param context:
    :return:
    """
    context.sym = symbol('originPrice')
    context.sym1 = symbol('updown')
    set_benchmark(symbol("originPrice"))
    context.hold = False


def handle_data(context, data):
    """
    zipline 에서 backtesting order 부분
    현재 전액을 사고 파는 형태로 되있다.
    :param context:
    :param data:
    :return:
    """
    buy = False
    sell = False
    pred_buy = data.current(context.sym1, 'close')
    pred_sell = data.current(context.sym1, 'volume')

    if pred_buy == 1 and context.hold == False:
        order_percent(context.sym, 0.99)
        context.hold = True
        buy = True
    elif pred_sell == 1 and context.hold == True:
        order_percent(context.sym, -0.99)
        context.hold = False
        sell = True
    record(originPrice=data.current(context.sym, "price"), buy=buy, sell=sell)


def backtesting(setting):
    """
    Zipline의 run-algorithm을 사용하는
    backtesting의 메인 부
    :param setting:
    :return:
    """

    cal = set_calendar(setting['calendar'])
    panel_data, start_date, end_date = setup_panel(setting['order_file_path'], setting['stock_name'])
    result = zipline.run_algorithm(start=start_date,
                                   end=end_date,
                                   initialize=initialize,
                                   trading_calendar=cal,
                                   capital_base=setting['start_value'],
                                   handle_data=handle_data,
                                   data=panel_data)
    result.rename(columns={'originPrice': setting['stock_name']}, inplace=True)
    result.to_csv(set_save_folder(os.curdir, 'backtesting') + '/' + setting['save_file_name'])
    print('backtesting done!')
    return result

if __name__ == '__main__':
    serial_info = {
        "order_file_path": '/home/jinjae/github/demoproject/save/order/DJI_order.csv',
        "save_file_name": 'test.csv',
        'stock_name': 'DJI',
        'start_value': int(1000) * 10000,
        'calendar': 'US'
    }
    panel_data, start_date, end_date = setup_panel(serial_info['order_file_path'], serial_info['stock_name'])

    print(panel_data)
    # print(panel_data['originPrice'])
    # print(panel_data['updown'])

    # start = datetime(2018, 1, 3, 0, 0, 0, 0, pytz.utc)
    # print(start)
    result = backtesting(serial_info)

    # panel = setup_panel('005930.csv', 'SAMSUNG')
    # print(panel[stock_name].index[0], panel[stock_name].index[-1])
    # print(panel[stock_name].index[0], panel[stock_name].index[-1])
    """
    start=datetime(2014, 12, 31, 0, 0, 0, 0, pytz.utc),
                                   end=datetime(2019, 11, 01, 0, 0, 0, 0, pytz.utc),
                                   """
