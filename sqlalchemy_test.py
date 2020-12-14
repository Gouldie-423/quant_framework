from sqlalchemy import create_engine
import yfinance as yf
import pandas as pd
from datetime import timedelta,datetime
import datetime as dt
from pandas_datareader import data as pdr
import csv
import config
import os
import config_test

pwd = 'Timphn123!'
engine = create_engine(f'postgresql://postgres:{pwd}@localhost/tradedatatest')

def uat_refresh_test():
	for i in config.tickers:
		try:
			func = ['daily','ma','macd','rsi']
			df=pdr.get_data_yahoo(i,dt.datetime(2010,1,1),dt.datetime(2019,12,31))
			df.insert(loc=0,column='ticker',value=i)
			for x in func:
				try:
					if x == 'daily':
						df.to_sql('daily_trade_data',engine,if_exists='replace',index=True)

					if x == 'ma':
						config_test.uat_ma_columns(df)
						config_test.remove_daily(df)
						df.to_sql('moving_averages',engine,if_exists='replace',index=True)
						
					if x == 'macd':
						config_test.uat_macd_columns(df)
						config_test.remove_daily(df)
						df.to_sql('macd',engine,if_exists='replace',index=True)
						
					if x == 'rsi':
						config_test.uat_rsi_columns(df)
						config_test.remove_daily(df)
						df.to_sql('rsi',engine,if_exists='replace',index=True)
						
					else:
						pass
					
				except KeyError:
					print(x)
		except KeyError:
			print(f'{i} was not pulled')

uat_refresh_test()