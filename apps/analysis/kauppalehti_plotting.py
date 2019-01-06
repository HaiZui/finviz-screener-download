#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Jan  6 20:49:49 2019

@author: haizui
"""


import invest_dw as idw
import invest_dw.database_etl as etl
import invest_dw.database_io as dio
import invest_dw.kauppalehti as kl
import pandas as pd
import matplotlib.pyplot as plt

ticker = 'NOKIA'

config = dio.readConfig('config_mysql.ini')

conn_sqlalch = dio.connectSqlalchemy(config)

xhel_prices = pd.read_sql_table('xhel_prices',schema='kauppalehti',con=conn_sqlalch)

xhel_prices['Valid_From_dt'] = pd.to_datetime(xhel_prices['Valid_From'],unit='s')
xhel_prices['Valid_To_dt'] = pd.to_datetime(xhel_prices['Valid_To'],unit='s')

xhel_dt = xhel_prices.set_index('Valid_From_dt')

# Plot
xhel_dt[xhel_dt['symbol'] == ticker]['lastPrice'].astype('float').plot() 

