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

			for x in func:

				if x == 'daily':
					df2 = df[['ticker','High','Low','Open','Close','Volume','Adj Close']]
					df2.to_sql('daily_trade_data',engine,if_exists='append',index=True)

				if x == 'ma':
					df2 = df[['ticker','200MA','150MA','100MA','75MA','50MA','35MA','25MA','15MA','10MA']]
					df2.to_sql('moving_averages',engine,if_exists='append',index=True)

				if x == 'macd':
					df2 = df[['ticker','MACD','Signal','MACDdiff','MACD-5D','Signal-5D','MACD-5Ddiff','MACD-10D',
					'Signal-10D','MACD-10Ddiff']]
					df2.to_sql('macd',engine,if_exists='append',index=True)

				if x == 'rsi':
					df2 = df[['ticker','50RSI','40RSI','30RSI','20RSI']]
					df2.to_sql('rsi',engine,if_exists='append',index=True)

				else:
					pass
			print(i)
					
		except KeyError:
			print(f'{i} was not pulled')

config.pull_SP_tickers()
uat_refresh_test()