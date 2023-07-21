# -*- coding:utf-8 -*-
"""
@File    : mongo_database.py
@Time    : 2023/7/18 23:57
@Author  : Chen GangQiang
@Contact : 644076531@qq.com
@Version : 1.0.0
@Desc    : 
"""

from pymongo import MongoClient

DB_CONN = MongoClient('mongodb://localhost:27017')['quant']
