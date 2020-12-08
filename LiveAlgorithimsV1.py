import pandas as pd
import numpy as np
import openpyxl
import csv
import config
import algorithims
from datetime import timedelta,datetime
import datetime as dt

today = datetime.now()
cd = today.strftime("%Y-%m-%d")
yesterday = today - timedelta(1)
yd = yesterday.strftime("%Y-%m-%d")
yr_ago = today - timedelta(330)

def v1():

	wb = openpyxl.Workbook()
	wb.create_sheet('Trade Data',0)
	trade_data = wb['Trade Data']
	excel_row = 2
	export_path = '/Users/timothygould/Google Drive/Quant Trading/Live Algorithims/'
	filename = f'Prod_v1{cd}.xlsx'

	for ticker in config.tickers:
			try:
				print(ticker)
				df = pd.read_csv(f'{config.prod_SP_path}{ticker}{cd}.csv')
				df.set_index('Date',inplace=True)
				config.prod_df_columns(df)
				n = -len(df.index)
				df['Buys'] = df['Adj Close']
				df['Sells'] = df['Adj Close']

			except FileNotFoundError:
				print(f'{ticker} not found')

			try:
				for i in df.index[n:]:
					algorithims.buy = None
					algorithims.sell = None
					days_open = []
					algorithims.buy_criteria_test(df,n)
					if algorithims.buy == True:
						n2=n
						for l in df.index[n2:]:
							algorithims.sell_criteria_v1(df,n,n2,algorithims.buy)
							n2=n2+1
							days_open.append(l)
							diff = ((df['Sells'][-1]/df['Buys'][n])-1)*100
							diff5 = ((df['Sells'][-1]/df['Buys'][-5])-1)*100
							diff10 = ((df['Sells'][-1]/df['Buys'][-10])-1)*100
						if algorithims.sell == True:
							break
						if algorithims.sell == None:
							algorithims.prod_export_v1(df,wb,trade_data,n,diff,
								diff5,diff10,ticker,excel_row,days_open,
								export_path,filename,i)
							excel_row = excel_row+1
							break
					n=n+1
			except UnboundLocalError:
				print('DB Not Refreshed. DF could not be created')

