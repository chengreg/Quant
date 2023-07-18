# -*- coding: utf-8 -*-
# @Time    : 2023/7/18 16:19
# @Author  : Chen GangQiang
# @Email   : uoaoo@163.com
# @File    : 最小市值选股.py
# @Software: PyCharm


import tushare as ts
import pandas as pd

pro = ts.pro_api('d689cb3c1d8c8a618e49ca0bb64f4d6de2f70e28ab5f76a867b31ac7')

# 获取A股股票列表
stocks = pro.daily_basic(ts_code='', trade_date='20230707', fields='trade_date,ts_code,close,pe,total_mv')

# 获取股票基础信息
stock_basic = pro.stock_basic(exchange='', list_status='L', fields='ts_code,name,market')

# 合并两个dateframe
df = pd.merge(stocks, stock_basic, on='ts_code')

# 去除ST股票
df = df[~df['name'].str.contains('ST')]

# 去除北交所
df = df[~df['market'].str.contains('北交所')]

# 去除退市
df = df[~df['name'].str.contains('退')]

# 根据市值排序获取最低的30支股票
df = df.sort_values('total_mv', ascending=True).head(30)

print(df)