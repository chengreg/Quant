# -*- coding: utf-8 -*-
# @Time    : 2023/7/18 17:29
# @Author  : Chen GangQiang
# @Email   : uoaoo@163.com
# @File    : tushareFeed.py
# @Software: PyCharm

import backtrader as bt
import tushare as ts
import datetime

tushare_token = "d689cb3c1d8c8a618e49ca0bb64f4d6de2f70e28ab5f76a867b31ac7"
pro = ts.pro_api(tushare_token)


class TushareData(bt.feed.DataBase):
    """
    TushareData base on pro.query('daily') interface,which is free for everyone
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # name of the table is indicated by dataname
        # data is fetch between fromdate and todate
        assert (self.p.fromdate is not None)
        assert (self.p.todate is not None)
        # iterator 4 data in the list
        self.iter = None
        self.data = None

    def start(self):
        if self.data is None:
            # query data from free interface
            self.data = pro.query('daily',
                                  ts_code=self.p.dataname,
                                  start_date=self.p.fromdate.strftime('%Y%m%d'),
                                  end_date=self.p.todate.strftime('%Y%m%d')
                                  )
            assert (self.data is not None)
        # set the iterator anyway
        self.iter = self.data.sort_index(ascending=False).iterrows()

    def stop(self):
        pass

    def _load(self):
        if self.iter is None:
            # if no data ... no parsing
            return False
        # try to get 1 row of data from iterator
        try:
            row = next(self.iter)
        except StopIteration:
            # end of the list
            return False
        # fill the lines
        self.lines.datetime[0] = self.date2num(datetime.datetime.strptime(row[1]['trade_date'], '%Y%m%d'))
        self.lines.open[0] = row[1]['open']
        self.lines.high[0] = row[1]['high']
        self.lines.low[0] = row[1]['low']
        self.lines.close[0] = row[1]['close']
        self.lines.volume[0] = row[1]['vol']
        self.lines.openinterest[0] = -1
        # Say success
        return True
