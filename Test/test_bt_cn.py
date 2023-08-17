# -*- coding: utf-8 -*-
# @Time    : 2023/8/17 14:34
# @Author  : Chen GangQiang
# @Email   : uoaoo@163.com
# @File    : test_bt_cn.py
# @Software: PyCharm

import backtrader_cn as bt

bt.Trade

if __name__ == '__main__':
    cerebro = bt.Cerebro()

    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    cerebro.run()

    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())