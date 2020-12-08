
import pandas as pd
import numpy as np
import openpyxl
import csv
import config
import algorithims

#Remember to check filename before you run! Don't want to override previous report. 

def tradesim():
	
	wb = openpyxl.Workbook()
	wb.create_sheet('Trade Data',0)
	trade_data = wb['Trade Data']
	excel_row = 2
	export_path = '/Users/timothygould/Desktop/'
	filename = 'matest.xlsx'
	
	for ticker in config.tickers:
		try:
			print(ticker)
			df = pd.read_csv(f'{config.uat_SP_path}{ticker}.csv')
			df.set_index('Date',inplace=True)
			config.uat_df_columns(df)
			n = -len(df.index)
			df['Buys'] = df['Adj Close']
			df['Sells'] = df['Adj Close']

		except FileNotFoundError:
			print(f'{ticker} not found')

		try:
			for i in df.index[n:]:
				algorithims.buy = None
				algorithims.sell = None
				holding_period = []
				algorithims.buy_criteria_v1(df,n)
				if algorithims.buy == True:
					n2=n
					for l in df.index[n2:]:
						algorithims.sell_criteria_v1(df,n,n2,algorithims.buy)
						n2=n2+1
						holding_period.append(l)
						if algorithims.sell == True:
							algorithims.uat_export_v1(i,l,algorithims.diff,
								export_path,filename,ticker,excel_row,
								holding_period,trade_data,wb)
							excel_row = excel_row+1
							break			
				n=n+1
		except KeyError:
			print('whoops')

config.pull_SP_tickers()
tradesim()
#Global Metrics
print(f'Win Ratio: {(len(algorithims.total_wins)/len(algorithims.total_trades))*100}%')
print(f'Number of Trades: {len(algorithims.total_trades)}')
print(f'Avg Holding Period: {sum(algorithims.global_holding_period)/len(algorithims.global_holding_period)} Days')
print(f'Avg Daily Increase: {sum(algorithims.avg_daily_return)/len(algorithims.avg_daily_return)}%')
print(f'Pct over .135: {(len(algorithims.pct_over_135)/len(algorithims.total_trades))*100}%')


