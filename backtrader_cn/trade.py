#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
###############################################################################
#
# Copyright (C) 2015-2023 Daniel Rodriguez
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import itertools

from .utils import AutoOrderedDict
from .utils.date import num2date
from .utils.py3 import range


class TradeHistory(AutoOrderedDict):
    '''Represents the status and update event for each update a Trade has
    表示每次交易更新的状态和更新事件的类

    This object is a dictionary which allows '.' notation
    此对象是一个字典，支持“.”标记法

    Attributes:
        属性
      - ``status`` (``dict`` with '.' notation): Holds the resulting status of
        an update event and has the following sub-attributes
        status``（带有“.”标记法的``dict``）：保存更新事件的结果状态，具有以下子属性

        - ``status`` (``int``): Trade status 交易状态
        - ``dt`` (``float``): float coded datetime 浮点编码的日期时间
        - ``barlen`` (``int``): number of bars the trade has been active 交易活动的时间点数量
        - ``size`` (``int``): current size of the Trade 交易的当前大小
        - ``price`` (``float``): current price of the Trade 交易的当前价格
        - ``value`` (``float``): current monetary value of the Trade 交易的当前货币价值
        - ``pnl`` (``float``): current profit and loss of the Trade 交易的当前盈亏
        - ``pnlcomm`` (``float``): current profit and loss minus commission 当前盈亏减去佣金

      - ``event`` (``dict`` with '.' notation): Holds the event update
        ``event``（带有“.”标记法的``dict``）：保存事件更新的
        - parameters 参数

        - ``order`` (``object``): the order which initiated the``update`` 发起``update``的订单
        - ``size`` (``int``): size of the update 更新的大小
        - ``price`` (``float``):price of the update 更新的价格
        - ``commission`` (``float``): price of the update 更新的佣金
    '''

    def __init__(self,
                 status, dt, barlen, size, price, value, pnl, pnlcomm, tz, event=None):
        '''Initializes the object to the current status of the Trade'''
        super(TradeHistory, self).__init__()
        self.status.status = status
        self.status.dt = dt
        self.status.barlen = barlen
        self.status.size = size
        self.status.price = price
        self.status.value = value
        self.status.pnl = pnl
        self.status.pnlcomm = pnlcomm
        self.status.tz = tz
        if event is not None:
            self.event = event

    def __reduce__(self):
        return (self.__class__, (self.status.status, self.status.dt, self.status.barlen, self.status.size,
                                 self.status.price, self.status.value, self.status.pnl, self.status.pnlcomm,
                                 self.status.tz, self.event, ))

    def doupdate(self, order, size, price, commission):
        '''Used to fill the ``update`` part of the history entry'''
        self.event.order = order
        self.event.size = size
        self.event.price = price
        self.event.commission = commission

        # Do not allow updates (avoids typing errors)
        self._close()

    def datetime(self, tz=None, naive=True):
        '''Returns a datetime for the time the update event happened'''
        return num2date(self.status.dt, tz or self.status.tz, naive)


class Trade(object):
    '''Keeps track of the life of an trade: size, price, commission (and value?)
    用于跟踪交易的生命周期的类：大小、价格、佣金（以及价值？）

    An trade starts at 0 can be increased and reduced and can be considered closed if it goes back to 0.
    交易从0开始，可以增加和减少，并且如果回到0，则被视为已关闭。

    The trade can be long (positive size) or short (negative size)
    交易可以是多头（正大小）或空头（负大小）

    An trade is not meant to be reversed (no support in the logic for it)
    交易不应被逆转（逻辑中不支持）

    Member Attributes:
    成员属性：

      - ``ref``: unique trade identifier 唯一的交易标识符
      - ``status`` (``int``): one of Created, Open, Closed 其中之一 Created、Open、Closed
      - ``tradeid``: grouping tradeid passed to orders during creation,The default in orders is 0
        在创建订单时传递给订单的交易标识,订单中的默认值为0
      - ``size`` (``int``): current size of the trade 交易的当前大小
      - ``price`` (``float``): current price of the trade 交易的当前价格
      - ``value`` (``float``): current value of the trade交易的当前价值
      - ``commission`` (``float``): current accumulated commission当前累积佣金
      - ``pnl`` (``float``): current profit and loss of the trade (gross pnl)交易的当前盈亏（总盈亏）
      - ``pnlcomm`` (``float``): current profit and loss of the trade minus
        commission (net pnl)
        交易的当前盈亏减去佣金（净盈亏）
      - ``isclosed`` (``bool``): records if the last update closed (set size to
        null the trade
        记录最后的更新是否关闭（将大小设置为空）
      - ``isopen`` (``bool``): records if any update has opened the trade 记录任何更新是否已开启交易
      - ``justopened`` (``bool``): if the trade was just opened 如果交易刚刚开启
      - ``baropen`` (``int``): bar in which this trade was opened 交易开启的时间点

      - ``dtopen`` (``float``): float coded datetime in which the trade was opened
        交易开启的浮点编码日期时间

        - Use method ``open_datetime`` to get a Python datetime.datetime
          使用方法 ``open_datetime`` 可以获取 Python datetime.datetime
          or use the platform provided ``num2date`` method
          或使用平台提供的 ``num2date`` 方法

      - ``barclose`` (``int``): bar in which this trade was closed 交易关闭的时间点

      - ``dtclose`` (``float``): float coded datetime in which the trade was closed

        - Use method ``close_datetime`` to get a Python datetime.datetime
          使用方法 ``close_datetime`` 可以获取 Python datetime.datetime
          or use the platform provided ``num2date`` method
          或使用平台提供的 ``num2date`` 方法

      - ``barlen`` (``int``): number of bars this trade was open 交易持续的时间点数量
      - ``historyon`` (``bool``): whether history has to be recorded 是否记录历史
      - ``history`` (``list``): holds a list updated with each "update" event 包含每个“update”事件更新的列表
        containing the resulting status and parameters used in the update 包含更新中的结果状态和参数

        The first entry in the history is the Opening Event
         历史中的第一个条目是开启事件
        The last entry in the history is the Closing Event
        史中的最后一个条目是关闭事件

    '''
    refbasis = itertools.count(1)

    status_names = ['Created', 'Open', 'Closed']
    Created, Open, Closed = range(3)

    def __str__(self):
        toprint = (
            'ref', 'data', 'tradeid',
            'size', 'price', 'value', 'commission', 'pnl', 'pnlcomm',
            'justopened', 'isopen', 'isclosed',
            'baropen', 'dtopen', 'barclose', 'dtclose', 'barlen',
            'historyon', 'history',
            'status')

        return '\n'.join(
            (':'.join((x, str(getattr(self, x)))) for x in toprint)
        )

    def __init__(self, data=None, tradeid=0, historyon=False,
                 size=0, price=0.0, value=0.0, commission=0.0):

        self.ref = next(self.refbasis)
        self.data = data
        self.tradeid = tradeid
        self.size = size
        self.price = price
        self.value = value
        self.commission = commission

        self.pnl = 0.0
        self.pnlcomm = 0.0

        self.justopened = False
        self.isopen = False
        self.isclosed = False

        self.baropen = 0
        self.dtopen = 0.0
        self.barclose = 0
        self.dtclose = 0.0
        self.barlen = 0

        self.historyon = historyon
        self.history = list()

        self.status = self.Created

    def __len__(self):
        '''Absolute size of the trade'''
        # 交易的绝对大小
        return abs(self.size)

    def __bool__(self):
        '''Trade size is not 0'''
        return self.size != 0

    __nonzero__ = __bool__

    def getdataname(self):
        '''Shortcut to retrieve the name of the data this trade references'''
        # 检索该交易引用的数据名称的快捷方式
        return self.data._name

    def open_datetime(self, tz=None, naive=True):
        '''Returns a datetime.datetime object with the datetime in which
        the trade was opened
        '''
        return self.data.num2date(self.dtopen, tz=tz, naive=naive)

    def close_datetime(self, tz=None, naive=True):
        '''Returns a datetime.datetime object with the datetime in which
        the trade was closed
        '''
        return self.data.num2date(self.dtclose, tz=tz, naive=naive)

    def update(self, order, size, price, value, commission, pnl,
               comminfo):
        '''
        Updates the current trade. The logic does not check if the
        trade is reversed, which is not conceptually supported by the
        object.

        If an update sets the size attribute to 0, "closed" will be
        set to true

        Updates may be received twice for each order, once for the existing
        size which has been closed (sell undoing a buy) and a second time for
        the the opening part (sell reversing a buy)

        Args:
            order: the order object which has (completely or partially)
                generated this update
            size (int): amount to update the order
                if size has the same sign as the current trade a
                position increase will happen
                if size has the opposite sign as current op size a
                reduction/close will happen

            price (float): always be positive to ensure consistency
            value (float): (unused) cost incurred in new size/price op
                           Not used because the value is calculated for the
                           trade
            commission (float): incurred commission in the new size/price op
            pnl (float): (unused) generated by the executed part
                         Not used because the trade has an independent pnl
        '''
        if not size:
            return  # empty update, skip all other calculations

        # Commission can only increase
        self.commission += commission

        # Update size and keep a reference for logic an calculations
        oldsize = self.size
        self.size += size  # size will carry the opposite sign if reducing

        # Check if it has been currently opened
        self.justopened = bool(not oldsize and size)

        if self.justopened:
            self.baropen = len(self.data)
            self.dtopen = 0.0 if order.p.simulated else self.data.datetime[0]
            self.long = self.size > 0

        # Any size means the trade was opened
        self.isopen = bool(self.size)

        # Update current trade length
        self.barlen = len(self.data) - self.baropen

        # record if the position was closed (set to null)
        self.isclosed = bool(oldsize and not self.size)

        # record last bar for the trade
        if self.isclosed:
            self.isopen = False
            self.barclose = len(self.data)
            self.dtclose = self.data.datetime[0]

            self.status = self.Closed
        elif self.isopen:
            self.status = self.Open

        if abs(self.size) > abs(oldsize):
            # position increased (be it positive or negative)
            # update the average price
            self.price = (oldsize * self.price + size * price) / self.size
            pnl = 0.0

        else:  # abs(self.size) < abs(oldsize)
            # position reduced/closed
            pnl = comminfo.profitandloss(-size, self.price, price)

        self.pnl += pnl
        self.pnlcomm = self.pnl - self.commission

        self.value = comminfo.getvaluesize(self.size, self.price)

        # Update the history if needed
        if self.historyon:
            dt0 = self.data.datetime[0] if not order.p.simulated else 0.0
            histentry = TradeHistory(
                self.status, dt0, self.barlen,
                self.size, self.price, self.value,
                self.pnl, self.pnlcomm, self.data._tz)
            histentry.doupdate(order, size, price, commission)
            self.history.append(histentry)
