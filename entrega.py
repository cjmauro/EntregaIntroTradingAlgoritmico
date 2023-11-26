from __future__ import (absolute_import, division, print_function, unicode_literals)
import datetime
import os.path
import sys

import backtrader as bt

class EstrellaDeTardetrategy(bt.Strategy):
    def next(self):
        if len(self) >= 3:
            if self.data.close[-3] > self.data.open[-3] and \
                self.data.close[-2] < self.data.open[-2] and \
                self.data.close[-1] > self.data.open[-1]:
                self.sell()
                
                
class HombreColgadoStrategy(bt.Strategy):
    def __init__(self):
        self.dataclose = self.datas[0].close
        self.datalow = self.datas[0].low

    def next(self):
        if self.dataclose[0] == self.datalow[0]:
            self.sell()

class RSIStrategy(bt.Strategy):
    params = (
        ("overbought", 70), 
        ("oversold", 30),
    )

    def __init__(self):
        self.rsi = bt.indicators.RelativeStrengthIndex()

    def next(self):
        if self.rsi < self.params.oversold:
            self.buy()

        elif self.rsi > self.params.overbought:
            self.sell()

class SellAfterDays(bt.Strategy):
    params = (
        ("sell_after_days", 6),
    )

    def __init__(self):
        self.days_since_buy = 0

    def next(self):
        if self.position:
            self.days_since_buy += 1 

            if self.days_since_buy == self.params.sell_after_days:
               
                self.sell()
                self.days_since_buy = 0 



if __name__ == '__main__':
    cerebro = bt.Cerebro()

    modpath = os.path.dirname(os.path.abspath(sys.argv[0]))
    datapath = os.path.join(modpath, 'datas', 'orcl-1995-2014.txt')

    data = bt.feeds.YahooFinanceCSVData(
        dataname=datapath,
        fromdate=datetime.datetime(2000, 1, 1),
        todate=datetime.datetime(2005, 12, 31),
        reverse=False
    )

    cerebro.adddata(data)
    cerebro.broker.set_cash(100000.0)
    cerebro.broker.setcommission(commission=0.001)

    cerebro.addstrategy(RSIStrategy, overbought=60, oversold=20)
    cerebro.addstrategy(HombreColgadoStrategy)
    cerebro.addstrategy(EstrellaDeTardetrategy)
    cerebro.addstrategy(SellAfterDays, sell_after_days=3)
    
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    cerebro.run()

    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
