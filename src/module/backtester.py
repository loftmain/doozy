import backtrader as bt
import datetime
 
# Your logic is inside this class :
class MyStrategy(bt.Strategy):
    params = (
        ('stop_loss', 0.02),
        ('take_profit', 0.04),
        ('period_rsi', 14),
        ('low_rsi', 20),
        ('high_rsi', 80)
    )
 
    def log(self, txt, dt=None):
        ''' Logging function for this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        time = self.datas[0].datetime.time()
        print('%s - %s, %s' % (dt.isoformat(), time, txt))
 
    def __init__(self):
        # Keep a reference to the "close"
        self.dataclose = self.datas[0].close
 
        # To keep track of pending orders and buy price/commission
        self.order = None
        self.buyprice = None
        self.buycomm = None
 
        # Add a RSI indicator
        self.rsi = bt.indicators.RelativeStrengthIndex(
            self.datas[0], period=self.params.period_rsi, safediv=True)
 
        self.price_at_signal = 0
        self.trades = 0
 
    def start(self):
        self.trades = 0
 
    def notify_trade(self, trade):
        if not trade.isclosed:
            return
 
        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
                 (trade.pnl, trade.pnlcomm))
 
    def notify_order(self, order):
        if order.status in [order.Margin, order.Rejected]:
            pass
 
        if order.status in [order.Submitted, order.Accepted]:
            # Order accepted by the broker. Do nothing.
            return
 
        elif order.status == order.Cancelled:
            self.log(' '.join(map(str, [
                'CANCEL ORDER. Type :', order.info['name'], "/ DATE :",
                self.data.num2date(order.executed.dt).date().isoformat(),
                "/ PRICE :",
                order.executed.price,
                "/ SIZE :",
                order.executed.size,
            ])))
 
        elif order.status == order.Completed:
            # If a stop loss or take profit is triggered:
            if 'name' in order.info:
                self.log("%s: REF : %s / %s / PRICE : %.3f / SIZE : %.2f / COMM : %.2f" %
                         (order.info['name'], order.ref,
                          self.data.num2date(order.executed.dt).date().isoformat(),
                          order.executed.price,
                          order.executed.size,
                          order.executed.comm))
 
            else:
                if order.isbuy():
                    # Initialize our take profit and stop loss orders :
                    stop_loss = order.executed.price * (1.0 - self.params.stop_loss)
                    take_profit = order.executed.price * (1.0 + self.params.take_profit)
 
                    stop_order = self.sell(exectype=bt.Order.StopLimit,
                                           price=stop_loss)
                    stop_order.addinfo(name="STOP")
 
                    #OCO : One cancels the Other => The execution of one instantaneously cancels the other
                    takeprofit_order = self.sell(exectype=bt.Order.Limit,
                                                 price=take_profit,
                                                 oco=stop_order)
                    takeprofit_order.addinfo(name="PROFIT")
 
                    self.log("SignalPrice : %.3f Buy: %.3f, Stop: %.3f, Profit : %.3f"
                             % (self.price_at_signal,
                                order.executed.price,
                                stop_loss,
                                take_profit))
 
                elif order.issell():
                    # As before, we initialize our stop loss and take profit here
                    stop_loss = order.executed.price * (1.0 + self.params.stop_loss)
                    take_profit = order.executed.price * (1.0 - self.params.take_profit)
 
                    stop_order = self.buy(exectype=bt.Order.StopLimit,
                                          price=stop_loss)
                    stop_order.addinfo(name="STOP")
 
                    #OCO !
                    takeprofit_order = self.buy(exectype=bt.Order.Limit,
                                                price=take_profit,
                                                oco=stop_order)
                    takeprofit_order.addinfo(name="PROFIT")
 
                    self.log("SignalPrice: %.3f Sell: %.3f, Stop: %.3f, Profit : %.3f"
                             % (self.price_at_signal,
                                order.executed.price,
                                stop_loss,
                                take_profit))
 
    def next(self):
        # Simply log the closing price and the current RSI value
        self.log('Close, %.3f / RSI : %.2f' % (self.dataclose[0], float(self.rsi[0])))
 
        # If I already have a pending order, I do nothing :
        if self.order:
            return
 
        # If I don't have any position I can take one:
        if self.position.size == 0:
            if self.rsi[0] >= self.params.high_rsi:
                # Sell short :
                self.sell()
                self.price_at_signal = self.dataclose[0]
                self.log('Sell order : %.3f' % self.dataclose[0])
                self.trades += 1
 
            elif self.rsi[0] <= self.params.low_rsi:
                # Go long :
                self.buy()
                self.price_at_signal = self.dataclose[0]
                self.log('Buy order : %.3f' % self.dataclose[0])
                self.trades += 1
 
            else:
                self.log("Nothing, wait.")
 
if __name__ == '__main__':
    cerebro = bt.Cerebro()
    # Setting my parameters : Stop loss at 1%, take profit at 4%, go short when rsi is 90 and long when 20.
    cerebro.addstrategy(strategy=MyStrategy, stop_loss=0.01, take_profit=0.04, high_rsi=90, low_rsi=20)
 
    data = bt.feeds.GenericCSVData(dataname="dependent/^DJI.csv",
                                   datetime=0,
                                   fromdate=datetime.datetime(2016, 1, 1),
                                   todate=datetime.datetime(2017, 10, 1),
                                   open=1,
                                   high=2,
                                   low=3,
                                   close=4,
                                   openinterest=-1,
                                   time=-1,
                                   volume=-1,
                                   timeframe=bt.TimeFrame.Minutes,
                                   compression=15,
                                   dtformat="%Y-%m-%d")
 
    cerebro.adddata(data)
 
    # no slippage
    cerebro.broker = bt.brokers.BackBroker(slip_perc=0.0)
 
    # 20 000$ cash initialization
    cerebro.broker.setcash(20000.0)
 
    # Add a FixedSize sizer according to the stake
    cerebro.addsizer(bt.sizers.FixedSize, stake=2)
 
    # Set the fees
    cerebro.broker.setcommission(commission=0.00005)
 
    # add analyzers
    cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name="mySharpe", riskfreerate=0.001)
    cerebro.addanalyzer(bt.analyzers.DrawDown, _name="myDrawDown")
 
    # Print out the starting conditions
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
 
    backtest = cerebro.run()
 
    # Print out the final result
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
 
    print('Sharpe Ratio:', backtest[0].analyzers.mySharpe.get_analysis())
    print('Drawdown :', backtest[0].analyzers.myDrawDown.get_analysis())
 
    cerebro.plot(style='candlestick', barup='green', bardown='red')