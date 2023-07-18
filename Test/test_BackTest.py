# -*- coding: utf-8 -*-
# @Time    : 2023/7/18 17:39
# @Author  : Chen GangQiang
# @Email   : uoaoo@163.com
# @File    : test_BackTest.py
# @Software: PyCharm
# -*- coding:utf-8 -*-

import backtrader as bt
from utils.BackTest import BackTestForSingleStock, BaseStrategy


class TestStrategy(BaseStrategy):
    def __init__(self):
        self.dataclose = self.datas[0].close

    def next(self):
        self.log('Close, %.2f' % self.dataclose[0])


if __name__ == '__main__':
    backtest = BackTestForSingleStock(TestStrategy, "601318.SH")
    backtest.run()
