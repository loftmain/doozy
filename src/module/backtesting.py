import pandas_datareader.data as web
import datetime
import matplotlib.pyplot as plt
from zipline.api import order_percent, record, symbol, order, order_target_percent, order_value, set_benchmark
from zipline.algorithm import TradingAlgorithm
import pandas as pd
from zipline.utils.factory import create_simulation_parameters
"""start = datetime.datetime(2010, 1, 1)
end = datetime.datetime(2016, 3, 29)
data = web.DataReader("AAPL", "yahoo", start, end)

data = data[['Adj Close']]
data.columns = ['AAPL']
data = data.tz_localize('UTC')"""




def initialize(context):
    context.sym = symbol('DJI')
    context.sym1 = symbol('buy')
    context.sym2 = symbol('sell')
    context.hold = False

def handle_data(context, data):
    buy = False
    sell = False

    pred_buy = data.current(context.sym1, 'price')
    pred_sell = data.current(context.sym2, 'price')

    if pred_buy == 1 and context.hold == False:
        order_percent(context.sym, 0.99)
        context.hold = True
        buy = True
    elif pred_sell == 1 and context.hold == True:
        order_percent(context.sym, -0.99)
        context.hold = False
        sell = True

    record(DJI=data.current(context.sym, "price"), buy=buy, sell=sell)

def backtesting(file):
    df = pd.read_excel(file)
    df["DATE"] = pd.to_datetime(df["DATE"])
    df = df.set_index("DATE")
    newdata = df[['Adj Close', "buy", 'sell']]
    newdata.columns = ['DJI', "buy", 'sell']

    newdata = newdata.tz_localize('UTC')
    algo = TradingAlgorithm(initialize = initialize, handle_data = handle_data)
    result = algo.run(newdata)
    result.to_csv("resultBacktesting.csv")
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
    result = backtesting("input_order.xlsx")
    plot_moneyflow(result)