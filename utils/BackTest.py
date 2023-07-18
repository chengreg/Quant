# -*- coding: utf-8 -*-
# @Time    : 2023/7/18 17:36
# @Author  : Chen GangQiang
# @Email   : uoaoo@163.com
# @File    : BackTest.py
# @Software: PyCharm

import time, datetime
import backtrader as bt
from utils.tushareFeed import TushareData


class BackTestForSingleStock:
    def __init__(self, strategy: bt.Strategy, code: str, start_date=None, end_date=None, cash=1000000.0,
                 commission=1 / 10000, isPlot=True):
        """
        回测主类
        :param strategy: 回测类名
        :param code: 股票代码
        :param start_date: 开始日期，不填写为730天之前
        :param end_date:结束日期，不填写为当日
        :param cash:初始资金，默认1000000
        :param commission:手续费，默认万1
        :param isPlot:是否显示图表，默认显示
        """
        self._strategy = strategy
        self._code = code
        self._cash = cash
        self._commission = commission
        self._isPlot = isPlot

        # 如果日期为空，获取1年之间的日期
        today = datetime.date.today()
        if start_date is None:
            self._start_date = today + datetime.timedelta(days=-730)
        else:
            self._start_date = self.StrToDate(start_date)
        if end_date is None:
            self._end_date = today
        else:
            self._end_date = self.StrToDate(end_date)

    def run(self):
        cerebro = bt.Cerebro()
        cerebro.addstrategy(self._strategy)

        # 获取tushare数据
        data = TushareData(dataname=self._code, fromdate=self._start_date, todate=self._end_date, )
        cerebro.adddata(data)

        cerebro.broker.setcash(self._cash)
        cerebro.broker.setcommission(commission=1 / 10000)

        print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
        cerebro.run()
        print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

        if self._isPlot:
            # 绘制蜡烛图
            params = dict(style='candle', barup='red', bardown='green', volup='red', voldown='green', )
            cerebro.plot(**params)

    def StrToDate(self, dateString):
        """
        字符串转日期格式
        :param dateString:
        :return:
        """
        date_str = dateString
        fmt = '%Y%m%d'
        time_tuple = time.strptime(date_str, fmt)
        year, month, day = time_tuple[:3]
        a_date = datetime.date(year, month, day)
        return a_date


class BaseStrategy(bt.Strategy):
    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))

                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:  # Sell
                self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
                 (trade.pnl, trade.pnlcomm))