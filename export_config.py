import csv
import numpy as np
import pandas as pd
import openpyxl
import csv
import config

#global variables that are shared between each function

total_wins = []
total_trades = []
global_holding_period = []
avg_daily_return = []
pct_over_135 = []

def sql_uat_export_v1(i,l,diff,ticker,holding_period,engine,alg_name):
	
	df = pd.DataFrame({'alg_name':alg_name,'ticker':ticker,
				'buy_date':i,
				'sell_date':l,
				'pct_diff':diff,
				'holding_period':len(holding_period),
				'pct_diff_avg':diff/len(holding_period)},
				index=[0])

	#used to store global metrics
	global_holding_period.append(len(holding_period))
	avg_daily_return.append(diff/len(holding_period))
	total_trades.append(diff)
	if diff >0:
		total_wins.append(diff)
	if (diff/len(holding_period))>.135:
		pct_over_135.append(diff/len(holding_period))
	else:
		pass
	
	df.to_sql('test_data',engine,if_exists = 'append',index=False)

def sql_prod_export_v1(df,l,diff,diff5,diff10,alg_name,ticker,days_open,i,engine,table):

	df = pd.DataFrame({'alg_name':alg_name,'ticker':ticker,
				'buy_date':i,
				'days_open':len(days_open),
				'diff_current':diff,
				'diff_5d':diff5,
				'diff_10d':diff10,
				'pct_diff_avg':diff/len(days_open)},
				index=[0])
	df.to_sql(table,engine,if_exists = 'append',index=False)
	
def closed_trade_export(i,l,diff,ticker,days_open,engine,alg_name,table):
	df = pd.DataFrame({'alg_name':alg_name,'ticker':ticker,
				'buy_date':i,
				'sell_date':l,
				'pct_diff':diff,
				'holding_period':len(days_open),
				'pct_diff_avg':diff/len(days_open)},
				index=[0])
	df.to_sql(table,engine,if_exists = 'append',index=False)

