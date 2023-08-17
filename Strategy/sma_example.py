# -*- coding: utf-8 -*-
# @Time    : 2023/8/17 12:03
# @Author  : Chen GangQiang
# @Email   : uoaoo@163.com
# @File    : sma_example.py
# @Software: PyCharm

import datetime
import backtrader as bt
from utils.tushareFeed import TushareData


# 策略类
class TestStrategy(bt.Strategy):
    params = (
        ('maperiod', 15),
    )

    def log(self, txt, dt=None):
        ''' 日志函数'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # 保留对 data[0] 数据系列中的 "close" 行的引用
        self.dataclose = self.datas[0].close

        # 跟踪未完成订单以及购买价格/佣金
        self.order = None
        self.buyprice = None
        self.buycomm = None

        # 添加一个简单移动平均（Moving Average Simple）指标
        self.sma = bt.indicators.SimpleMovingAverage(self.datas[0], period=self.p.maperiod)

    def notify_order(self, order):
        # 检查订单状态是否为"Submitted"（已提交）或"Accepted"（已接受），如果是，则不做任何操作，直接返回
        if order.status in [order.Submitted, order.Accepted]:
            return

        #  订单已完全成交
        if order.status in [order.Completed]:
            if order.isbuy():
                # order.executed.price：这个属性表示订单执行时的价格。对于买入订单，它表示成交的价格；对于卖出订单，它也表示成交的价格。
                # order.executed.value：这个属性表示订单实际成交的总价值。对于买入订单，它等于order.executed.price * 订单的数量；对于卖出订单，它也等于order.executed.price * 订单的数量
                self.log(f"买入执行, 买入价格: {order.executed.price:.2f}, Cost: {order.executed.value:.2f}, 佣金: {order.executed.comm:.2f}")

                # self.buyprice = order.executed.price
                # self.buycomm = order.executed.comm
            else:
                self.log(f"卖出执行, 卖出价格: {order.executed.price:.2f}, Cost: {order.executed.value:.2f}, 佣金: {order.executed.comm:.2f}")

            # 将当前的数据点（bar）的索引值（长度len(self)）赋值给self.bar_executed属性
            # 在Backtrader中，策略类会在每个新的数据点（bar）到来时被调用，这就意味着len(self)表示当前策略已经处理的数据点数量。
            # self.bar_executed = len(self)

        # 订单状态是否为取消、资金不足、被拒绝
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('订单 被取消/资金不足/被拒绝')

        self.order = None

    def notify_trade(self, trade):
        """
        用于在交易关闭时被调用。它接受一个 trade 参数，该参数表示被关闭的交易对象
        :param trade:该参数表示被关闭的交易对象
        """
        # 如果交易没有被关闭
        if not trade.isclosed:
            return

        # trade.pnl 表示交易的利润
        # trade.pnlcomm 表示交易的净利润（扣除佣金）
        self.log(f"交易利润， 毛利: {trade.pnl:.2f}, 净利: {trade.pnlcomm:.2f}")

    def next(self):
        self.log('Close, %.2f' % self.dataclose[0])

        # 如果存在未处理的订单（self.order 不为 None），则直接返回，不再执行下面的代码
        if self.order:
            return

        # 如果没有持仓
        if not self.position:
            if self.dataclose[0] > self.sma[0]:
                self.log('BUY CREATE, %.2f' % self.dataclose[0])

                # 确保没有未处理的订单时执行买入操作，并通过将订单对象保存在 self.order 中，避免在之后的操作中重复下单
                self.order = self.buy()

        else:

            if self.dataclose[0] < self.sma[0]:
                self.log('SELL CREATE, %.2f' % self.dataclose[0])
                self.order = self.sell()


if __name__ == '__main__':
    # 创建一个 Backtrader 引擎实例
    cerebro = bt.Cerebro()

    # 将一个策略添加到 Backtrader 的引擎中
    cerebro.addstrategy(TestStrategy)

    # 自定义tushare的数据源(Data Feed)
    data = TushareData(dataname="601318.sh", fromdate=datetime.date(2023, 1, 1), todate=datetime.date(2023, 8, 1), )
    # 将数据源添加到 Backtrader 的引擎实例中
    cerebro.adddata(data)

    # 设置回测或交易的初始资金量
    cerebro.broker.setcash(1000.0)

    # 固定数量大小，stake表示每次交易的数量
    cerebro.addsizer(bt.sizers.FixedSize, stake=15)

    # 设置交易佣金
    cerebro.broker.setcommission(commission= 2/10000)

    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    cerebro.run()

    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
