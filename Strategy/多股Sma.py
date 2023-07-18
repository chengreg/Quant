# -*- coding:utf-8 -*-
"""
@File    : 多股sma.py
@Time    : 2023/2/7 02:47
@Author  : Chen GangQiang
@Contact : 644076531@qq.com
@Version : 1.0.0
@Desc    :
"""

import backtrader as bt


class SmaCross(bt.Strategy):
    # 定义参数
    params = dict(
        fast_period=5,  # 快速移动平均期数
        slow_period=10, )  # 慢速移动平均期数

    def __init__(self):
        # 股票stock的快速移动平均线指标
        fastMA = {stock: bt.ind.MovingAverageSimple(stock, period=self.params.fast_period) for stock in self.datas}

        # 股票stock的慢速移动平均线指标
        slowMA = {stock: bt.ind.MovingAverageSimple(stock, period=self.params.slow_period) for stock in self.datas}

        # 股票stock的移动均线交叉信号指标
        self.crossover = {stock: bt.ind.CrossOver(fastMA[stock], slowMA[stock]) for stock in self.datas}

        self.orderlist = []  # 以往订单列表

    def next(self):  # 每个新bar触发调用一次，相当于其他框架的 on_bar()方法
        for o in self.orderlist:
            self.cancel(o)  # 取消以往所有订单
            self.orderlist = []  # 置空

        for stock in self.datas:
            if not self.getposition(stock):  # 还没有仓位，才可以买
                if self.crossover[stock] > 0:  # 金叉
                    order = self.buy(data=stock, size=100)
                    self.orderlist.append(order)

            # 已有仓位，才可以卖
            elif self.crossover[stock] < 0:  # 死叉
                order = self.sell(data=stock, size=100)
                self.orderlist.append(order)