import csv
import numpy as np
import pandas as pd
import openpyxl
import csv
import config

#global variables that are shared between each function

buy = None
sell = None

diff = 0

total_wins = []
total_trades = []
global_holding_period = []
avg_daily_return = []
pct_over_135 = []


def buy_criteria_v1(df,n):
		RSI_Lookback = []
		if df['35MA'][n]<df['50MA'][n] and df['35MA'][n-1]>df['50MA'][n-1]:
			pass
			if df['MACD-10Ddiff'][n]<df['MACD-5Ddiff'][n]<df['MACDdiff'][n]:
				pass
				if df['MACD-5Ddiff'][n]-df['MACD-10Ddiff'][n]>0.4:
					pass
					for x in df[f'20RSI'][n-20:n]:
						if x < 30:
							RSI_Lookback.append(x)
					if len(RSI_Lookback) > 0 and df[f'30RSI'][n]>30:
						global buy
						buy = True
						return buy

def buy_criteria_test(df,n):
		RSI_Lookback = []
		if df['35MA'][n]<df['50MA'][n] and df['35MA'][n-1]>df['50MA'][n-1]:
			pass
			if df['MACD-10Ddiff'][n]<df['MACD-5Ddiff'][n]<df['MACDdiff'][n]:
				global buy
				buy = True
				return buy

def sell_criteria_v1(df,n,n2,buy):
	if df['15MA'][n2]>df['35MA'][n2] and df['15MA'][n2-1]<df['35MA'][n2-1]:
		global diff
		diff = ((df['Sells'][n2]/df['Buys'][n])-1)*100
		global sell
		sell = True
		return sell
		return diff

def uat_export_v1(i,l,diff,export_path,filename,ticker,
	excel_row,holding_period,trade_data,wb):
	
	#standard export rows
	trade_data['A1'] = 'Ticker'
	trade_data[f'A{excel_row}'] = ticker
	trade_data['B1'] = 'Buy Date'
	trade_data[f'B{excel_row}'] = i
	trade_data['C1'] = 'Sell Date'
	trade_data[f'C{excel_row}'] = l
	trade_data['D1'] = 'Holding Period'
	trade_data[f'D{excel_row}'] = len(holding_period)
	trade_data['E1'] = '% Change'
	trade_data[f'E{excel_row}'] = diff
	trade_data['F1'] = 'Avg % Change'
	trade_data[f'F{excel_row}'] = diff/len(holding_period)
	#add any custom rows below here

	#Global Data to return in terminal
	global_holding_period.append(len(holding_period))
	avg_daily_return.append(diff/len(holding_period))
	total_trades.append(diff)
	if diff >0:
		total_wins.append(diff)
	if (diff/len(holding_period))>.135:
		pct_over_135.append(diff/len(holding_period))
	else:
		pass
	#save workbook after each trade has been made
	wb.save(f'{export_path}{filename}')


def prod_export_v1(df,wb,trade_data,n,diff,diff5,diff10,
	ticker,excel_row,days_open,export_path,filename,i):
	
	trade_data['A1'] = 'Ticker'
	trade_data[f'A{excel_row}'] = ticker
	trade_data['B1'] = 'Buy Date'
	trade_data[f'B{excel_row}'] = i
	trade_data['C1'] = 'Buy Price'
	trade_data[f'C{excel_row}'] = df['Buys'][n]
	trade_data['D1'] = 'Current Date'
	trade_data[f'D{excel_row}'] = df.index[-1]
	trade_data['E1'] = 'Days Open'
	trade_data[f'E{excel_row}'] = len(days_open)
	trade_data['F1'] = '% Change'
	trade_data[f'F{excel_row}'] = diff
	trade_data['G1'] = 'Avg % Change'
	trade_data[f'G{excel_row}'] = diff/len(days_open)
	if len(days_open)>5:
		trade_data['H1'] = '% Change last 5D'
		trade_data[f'H{excel_row}'] = diff5
	if len(days_open)>10:
		trade_data['I1'] = '% Change last 10D'
		trade_data[f'I{excel_row}'] = diff10


	wb.save(f'{export_path}{filename}')


	

