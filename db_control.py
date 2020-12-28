from sqlalchemy import create_engine
import yfinance as yf
import pandas as pd
from datetime import timedelta,datetime
import datetime as dt
from pandas_datareader import data as pdr
import config
import uat_config as uat
import prod_config as prod

today = datetime.now()
cd = today.strftime("%Y-%m-%d")
yesterday = today - timedelta(1)
yd = yesterday.strftime("%Y-%m-%d")
yr_ago = today - timedelta(365)

local = False #True = local db, False = server db
backtest = True #True = uat tables/2010-2019 timeframe, False = prod tables/recent timeframe
refresh = False #True = takes last row, False

#backtest = True & refresh = False should only occur when initializing prod db
#otherwise those should always be True/True


def run():
	for i in config.tickers:

		logic_tree_p2(logic_tree_p1(backtest,i),local,backtest,refresh)

def pull_data(begin_date,end_date,i):
#pulling in df to set baseline for outstanding shares
	df3=pdr.get_data_yahoo(i,dt.datetime(2020,12,23),dt.datetime(2020,12,24))
	mkt_cap = pdr.get_quote_yahoo(i)['marketCap']
	outstanding_shares = mkt_cap/df3['Adj Close'][-1]
	#pulling in rest of data	
	df=pdr.get_data_yahoo(i,begin_date,end_date)
	uat.uat_df_columns(df,outstanding_shares)
	#adjusting df before importing to db
	df.insert(0,'ticker',i) #putting ticket at beginning
	df = df.reset_index() #date as index (to rename it)
	config.rename_df_columns(df) #renaming columns so they are query-able in sql
	df = df.set_index("date") #adding date back in as index
	print(i)
	return df

def write_data(data,engine,prefix):
	func = ['daily','ma','macd','rsi']

	for x in func:

		if x == 'daily':
			df = data[['ticker','high','low','open','close','volume','mkt_cap','adj_close']]
			df.to_sql(f'{prefix}_daily_trade_data',engine,if_exists='append',index=True)

		if x == 'ma':
			df = data[['ticker','ma200','ma150','ma100','ma75','ma50','ma35',
			'ma25','ma15','ma10']]
			df.to_sql(f'{prefix}_moving_averages',engine,if_exists='append',index=True)

		if x == 'macd':
			df = data[['ticker','macd','signal','macd_diff','macd_5d','signal_5d',
			'macd_5diff','macd_10d','signal_10d','macd_10diff']]
			df.to_sql(f'{prefix}_macd',engine,if_exists='append',index=True)

		if x == 'rsi':
			df = data[['ticker','rsi50','rsi40','rsi30','rsi20']]
			df.to_sql(f'{prefix}_rsi',engine,if_exists='append',index=True)

		else:
			pass
	
	return prefix

def logic_tree_p1(backtest,i):

	if backtest == True:
		begin_date = dt.datetime(2010,1,1)
		end_date = dt.datetime(2019,12,31)
		data = pull_data(begin_date,end_date,i)

	else:
		begin_date = yr_ago
		end_date = datetime.now()
		data = pull_data(begin_date,end_date,i)
	
	return data


def logic_tree_p2(data,local,backtest,refresh):
	if refresh == True:
		data = data.tail(1)
		if local == True and backtest == True:
			engine = config.localengine
			write_data(data,engine,'bt')

		if local == True and backtest != True:
			engine = config.localengine
			write_data(data,engine,'lv')

		if local != True and backtest == True:
			engine = config.serverengine
			write_data(data,engine,'bt')

		if local != True and backtest != True:
			engine = config.serverengine
			write_data(data,engine,'lv')

	else:
		if local == True and backtest == True:
			engine = config.localengine
			write_data(data,engine,'bt')

		if local == True and backtest != True:
			engine = config.localengine
			write_data(data,engine,'lv')

		if local != True and backtest == True:
			engine = config.serverengine
			write_data(data,engine,'bt')

		if local != True and backtest != True:
			engine = config.serverengine
			write_data(data,engine,'lv')

	return data,engine

config.pull_SP_tickers()
run()
