import matplotlib.pyplot as plt
import pandas as pd
from zipline.algorithm import TradingAlgorithm
from zipline.api import record, symbol, order_percent

df = pd.read_excel("input_simulate.xlsx")
df["Date"] = pd.to_datetime(df["Date"])
df = df.set_index("Date")
newdata = df[['Adj Close', "buy", 'sell']]
newdata.columns = ['DJI', "buy", 'sell']

newdata = newdata.tz_localize('UTC')


def initialize(context):
    context.dji = symbol('DJI')
    context.buy = symbol('buy')
    context.sell = symbol('sell')

def handle_data(context, data):

    buy = False
    sell = False

    buy = data.current(context.buy, 'price')
    sell = data.current(context.sell, 'price')
    
    if buy == 1:
        order_percent(context.dji, 0.99)
        buy = True
    elif sell == 1:
        order_percent(context.dji, -0.99)
        sell = True

    record(DJI=data.current(context.dji, "price"), buy=buy, sell=sell)

algo = TradingAlgorithm(initialize=initialize, handle_data=handle_data)
result = algo.run(newdata)

#plt.plot(result.index, result.ma5)
#plt.plot(result.index, result.ma20)
ax = plt.plot(result.index, result.portfolio_value)
plt.legend(loc='best')

plt.plot(result.ix[result.buy == True].index, result.portfolio_value[result.buy == True], '^')
plt.plot(result.ix[result.sell == True].index, result.portfolio_value[result.sell == True], 'v')

plt.show()

#print(result[['starting_cash', 'ending_cash', 'ending_value']])

result.to_csv("result.csv")