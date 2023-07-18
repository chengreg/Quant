# -*- coding: utf-8 -*-
# @Time    : 2023/7/18 16:11
# @Author  : Chen GangQiang
# @Email   : uoaoo@163.com
# @File    : tushare_test.py
# @Software: PyCharm

import tushare as ts
import pandas as pd

pro = ts.pro_api('d689cb3c1d8c8a618e49ca0bb64f4d6de2f70e28ab5f76a867b31ac7')

df = pro.daily(ts_code='000001.SZ', start_date='20180701', end_date='20180718')

print(df)