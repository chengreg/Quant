# -*- coding:utf-8 -*-
"""
@File    : get_data_from_baostock.py
@Time    : 2023/7/22 02:45
@Author  : Chen GangQiang
@Contact : 644076531@qq.com
@Version : 1.0.0
@Desc    : 
"""
import pandas as pd
import baostock as bs


def get_data_from_baostock(code, start_date, end_date, freq='d', adjustflag='3'):
    lg = bs.login()

    if str(code)[0] == '6':
        code = 'sh.' + code
    else:
        code = 'sz.' + code

    if freq in ['d', 'w', 'm']:
        fields = 'date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,pctChg'
    else:
        fields = 'date,time,code,open,high,low,close,volume,amount,adjustflag'

    # 接口地址：http://baostock.com/baostock/index.php/A%E8%82%A1K%E7%BA%BF%E6%95%B0%E6%8D%AE
    rs = bs.query_history_k_data_plus(code,
                                      fields,
                                      start_date=start_date,
                                      end_date=end_date,
                                      frequency=str(freq),
                                      adjustflag=str(adjustflag)) # 复权类型，默认不复权：3；1：后复权；2：前复权。

    df = pd.DataFrame(rs.data, columns=fields.split(','))

    bs.logout()

    return df


if __name__ == '__main__':
    df = get_data_from_baostock('000001', '2018-07-01', '2018-07-18', freq='5', adjustflag='3')
    print(df)
