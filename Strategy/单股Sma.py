# -*- coding:utf-8 -*-
"""
@File    : sma.py
@Time    : 2023/2/5 22:42
@Author  : Chen GangQiang
@Contact : 644076531@qq.com
@Version : 1.0.0
@Desc    :
"""

import backtrader as bt
from utils.BackTest import BackTestForSingleStock, BaseStrategy


class SmaCross(BaseStrategy):
    # 定义参数
    params = dict(pfast=5, pslow=30)

    def __init__(self):
        self.dataclose = self.datas[0].close

        sma1 = bt.ind.SMA(period=self.p.pfast)
        sma2 = bt.ind.SMA(period=self.p.pslow)
        self.crossover = bt.ind.CrossOver(sma1, sma2)

        self.order = None

    def next(self):
        self.cancel(self.order)  # 取消以往未执行订单

        if not self.position:
            if self.crossover > 0:  # 金叉
                self.log('BUY CREATE, %.2f' % self.dataclose[0])
                self.order = self.buy(size=10000)

        elif self.crossover < 0:  # 死叉
            self.log('SELL CREATE, %.2f' % self.dataclose[0])
            self.order = self.sell(size=10000)


if __name__ == '__main__':
    backtest = BackTestForSingleStock(SmaCross, '000036.SZ')
    backtest.run()