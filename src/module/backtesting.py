from collections import OrderedDict
from datetime import datetime

import matplotlib.pyplot as plt
import pandas as pd
import pytz
import zipline
from trading_calendars import get_calendar
from zipline.api import order_percent, record, symbol, set_benchmark

path = '005930.csv'
stock_name = 'SAMSUNG'


def setup_panel(path, stock_name):
    file_path = path
    data = OrderedDict()
    data[stock_name] = pd.read_csv(file_path, index_col=0, parse_dates=['date'])
    data[stock_name] = data[stock_name][["open", "high", "low", "close", "volume"]]
    data['updown'] = pd.read_csv(file_path, index_col=0, parse_dates=['date'])
    data['updown']['null1'] = 0
    data['updown']['null2'] = 0
    data['updown']['null3'] = 0
    data['updown'] = data['updown'][["null1", "null2", "null3", "buy", "sell"]]
    data['updown'].rename(columns={"null1": "open",
                                   "null2": "high",
                                   "null3": "low",
                                   "buy": "close",
                                   "sell": "volume"}, inplace=True)
    panel = pd.Panel(data)
    panel.minor_axis = ["open", "high", "low", "close", "volume"]
    panel.major_axis = panel.major_axis.tz_localize(pytz.utc)
    return panel


def initialize(context):
    context.sym = symbol('SAMSUNG')
    context.sym1 = symbol('updown')
    set_benchmark(symbol("SAMSUNG"))
    context.hold = False

def handle_data(context, data):
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


def backtesting(file_path, name, output_name):
    korea_calendar = get_calendar('XKRX')
    result = zipline.run_algorithm(start=datetime(2018, 1, 3, 0, 0, 0, 0, pytz.utc),
                                   end=datetime(2019, 12, 30, 0, 0, 0, 0, pytz.utc),
                                   initialize=initialize,
                                   trading_calendar=korea_calendar,
                                   capital_base=10000000,
                                   handle_data=handle_data,
                                   data=setup_panel(file_path, name))
    result.rename(columns={'originPrice': name}, inplace=True)
    result.to_csv(output_name)
    return result

def plot_moneyflow(result):

    #plt.plot(result.index, result.ma5)
    ax1 = plt.plot(result.index, result.portfolio_value)
    plt.legend(loc='best')

    plt.plot(result.ix[result.buy == True].index, result.portfolio_value[result.buy == True], '^')
    plt.plot(result.ix[result.sell == True].index, result.portfolio_value[result.sell == True], 'v')

    plt.show()

    print(result[['starting_cash', 'ending_cash', 'ending_value']])
    print(result['portfolio_value'][-1]/result['portfolio_value'][0])


if __name__ == '__main__':
    result = backtesting('005930.csv', 'SAMSUNG', 'SAMSUNG_RESULT.csv')
    plot_moneyflow(result)

    # setup_panel('005930.csv', 'SAMSUNG')
