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
			config.uat_df_columns(df)
			df.insert(0,'ticker',i)
			#adjusting df before importing to db
			df = df.reset_index()
			config.rename_df_columns(df)
			df = df.set_index("date")

			print(i)

			for x in func:

				if x == 'daily':
					df2 = df[['ticker','high','low','open','close','volume','adj_close']]
					df2.to_sql('daily_trade_data',engine,if_exists='append',index=True)

				if x == 'ma':
					df2 = df[['ticker','ma200','ma150','ma100','ma75','ma50','ma35',
					'ma25','ma15','ma10']]
					df2.to_sql('moving_averages',engine,if_exists='append',index=True)

				if x == 'macd':
					df2 = df[['ticker','macd','signal','macd_diff','macd_5d','signal_5d',
					'macd_5diff','macd_10d','signal_10d','macd_10diff']]
					df2.to_sql('macd',engine,if_exists='append',index=True)

				if x == 'rsi':
					df2 = df[['ticker','rsi50','rsi40','rsi30','rsi20']]
					df2.to_sql('rsi',engine,if_exists='append',index=True)

				else:
					pass
		
		except KeyError:
			print(f'{i} was not pulled')

uat_refresh_test()