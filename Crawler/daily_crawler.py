# -*- coding:utf-8 -*-
"""
@File    : daily_crawler.py
@Time    : 2023/7/18 23:59
@Author  : Chen GangQiang
@Contact : 644076531@qq.com
@Version : 1.0.0
@Desc    : 
"""

import tuShare as ts
from Database.mongo_database import DB_CONN
from datetime import datetime


class DailyCrawler:
    def __init__(self):
        self.daily = DB_CONN['daily']
        self.daily_hfq = DB_CONN['daily_hfq']

    def crawl_index(self, begin_date=None, end_date=None):
        """
        获取指数的日线行情
        :param begin_date: 开始日期
        :param end_date: 结束日期
        :return:
        """
        index_codes = ['000001', '000300', '399001', '399005', '399006']

        now = datetime.now().strftime('%Y-%m-%d')

        if begin_date is None:
            begin_date = now
        if end_date is None:
            end_date = now

        for code in index_codes:
            df_daily = ts.pro_bar(ts_code='{}.SH'.format(code), asset='I', start_date=begin_date, end_date=end_date)
            df_daily = df_daily.sort_values('trade_date', ascending=True)
            df_daily.index = range(df_daily.shape[0])
            
            for index in range(df_daily.shape[0]):
                doc = dict(df_daily.loc[index])
                doc['index'] = code
                self.daily_hfq.insert_one(doc)