import pandas as pd
import numpy as np
import openpyxl
import csv
import config
import export_config as export
from datetime import timedelta,datetime
import datetime as dt
import prod_config as prod
import timeit

today = datetime.now()
cd = today.strftime("%Y-%m-%d")
yesterday = today - timedelta(1)
yd = yesterday.strftime("%Y-%m-%d")
yr_ago = today - timedelta(330)

local = True
buytest = []
selltest = []

def run(local):
	if local == True:
		config.localengine.execute('DELETE FROM open_trades')
		print('open trades refreshed')
		open_trades(config.localengine)
		closed_trades(config.localengine)

	else:
		config.serverengine.execute('DELETE FROM open_trades')
		print('open trades refreshed')
		open_trades(config.serverengine)
		closed_trades(config.serverengine)


def closed_trades(engine):
	alg_name = 'V2'
	for ticker in config.tickers:
			try:
				df = prod.grab_sql(ticker,engine)
				df.set_index('date',inplace=True)
				buysearch = -len(df.index)
				df['Buys'] = df['adj_close']
				df['Sells'] = df['adj_close']
				print(ticker)
			except FileNotFoundError:
				print(f'{ticker} not found')
			try:
				for i in df.index[buysearch:]:
					days_open = []
					buy = prod.buy_criteria_v2(df,buysearch)
					if buy == True:
						buytest.append('yay')
						sellsearch = buysearch
						for l in df.index[sellsearch:]:
							sell = prod.sell_criteria_v1(df,sellsearch)
							days_open.append(l)
							if sell == True:
								dupe_trade_check =  pd.read_sql_query(f"SELECT alg_name,ticker,buy_date FROM prev_trades WHERE ticker = '{ticker}' AND buy_date = '{i}' AND alg_name = '{alg_name}'",engine)
								if len(dupe_trade_check) > 0:
									break
								else:
									diff = ((df['Sells'][sellsearch]/df['Buys'][buysearch])-1)*100
									export.closed_trade_export(i,l,diff,ticker,days_open,engine,alg_name,'prev_trades')
									break
							sellsearch=sellsearch+1
					buysearch=buysearch+1


			except UnboundLocalError:
				print('DB Not Refreshed. DF could not be created')
def open_trades(engine):
	alg_name = 'V2'
	for ticker in config.tickers:
			try:
				df = prod.grab_sql(ticker,engine)
				df.set_index('date',inplace=True)
				buysearch = -len(df.index)
				df['Buys'] = df['adj_close']
				df['Sells'] = df['adj_close']
				print(ticker)
			except FileNotFoundError:
				print(f'{ticker} not found')
			try:
				for i in df.index[buysearch:]:
					days_open = []
					buy = prod.buy_criteria_v2(df,buysearch)
					if buy == True:
						buytest.append('yay')
						sellsearch = buysearch
						for l in df.index[sellsearch:]:
							sell = prod.sell_criteria_v1(df,sellsearch)
							days_open.append(l)
							sellsearch=sellsearch+1
							if sell == True:
								selltest.append('boo')
								break
						if buy == True and sell == None:
							diff = ((df['Sells'][-1]/df['Buys'][buysearch])-1)*100
							diff5 = ((df['Sells'][-1]/df['Buys'][-5])-1)*100
							diff10 = ((df['Sells'][-1]/df['Buys'][-10])-1)*100
							export.sql_prod_export_v1(df,l,diff,diff5,diff10,alg_name,ticker,days_open,i,engine,'open_trades')
						
					buysearch=buysearch+1


			except UnboundLocalError:
				print('DB Not Refreshed. DF could not be created')

config.pull_SP_tickers()
run(local)
print(len(buytest))
print(len(selltest))
execution_time = timeit.timeit(code, number=1)
print(execution_time)
