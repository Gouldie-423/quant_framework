
import pandas as pd
import numpy as np
import openpyxl
import csv
import config
import export_config as export
import uat_config as uat
from sqlalchemy import create_engine
import timeit

#Remember to check filename before you run! Don't want to override previous report. 
local = True

def run(local):
	if local == True:
		tradesim(config.localengine)
	else:
		tradesim(config.serverengine)

def tradesim(engine):
	alg_name = 'V1'
	
	for ticker in config.tickers:
		try:
			
			print(ticker)
			df = uat.grab_sql(ticker,engine)
			df.set_index('date',inplace=True)
			buysearch = -len(df.index)
			df['buys'] = df['adj_close']
			df['sells'] = df['adj_close']

		except FileNotFoundError:
			print(f'{ticker} not found')

		try:
			for i in df.index[buysearch:]:
				holding_period = []
				buy = uat.buy_criteria_v1(df,buysearch)
				if buy == True:
					sellsearch=buysearch
					for l in df.index[sellsearch:]:
						sell = uat.sell_criteria_v1(df,sellsearch)
						holding_period.append(l)
						if sell == True:
							diff = ((df['sells'][sellsearch]/df['buys'][buysearch])-1)*100
							export.sql_uat_export_v1(i,l,diff,ticker,holding_period,engine,alg_name)
							break			
						sellsearch=sellsearch+1
				buysearch=buysearch+1
		except TypeError:
			print(f'{ticker} not processed')

#Global Metrics
	df = pd.DataFrame({'alg_name':alg_name,'win_ratio':(len(export.total_wins)/len(export.total_trades)*100),
					'num_trades':len(export.total_trades),
					'avg_holding_period':sum(export.global_holding_period)/len(export.global_holding_period),
					'avg_daily_increase':sum(export.avg_daily_return)/len(export.avg_daily_return),
					'over_135':(len(export.pct_over_135)/len(export.total_trades)*100)},
					index=[0])

	df.to_sql('global_test_data',engine,if_exists='replace',index=False)

config.pull_SP_tickers()
execution_time = timeit.timeit(run(local), number=1)
print(execution_time)
