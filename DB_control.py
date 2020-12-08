import yfinance as yf
import pandas as pd
from datetime import timedelta,datetime
import datetime as dt
from pandas_datareader import data as pdr
import csv
import config
import os

today = datetime.now()
cd = today.strftime("%Y-%m-%d")
yesterday = today - timedelta(1)
yd = yesterday.strftime("%Y-%m-%d")
yr_ago = today - timedelta(330)


def uat_refresh(path):
	for i in config.tickers:
		if not (os.path.exists(f'{path}{i}.csv')):
			try:
				df=pdr.get_data_yahoo(i,dt.datetime(2010,1,1),dt.datetime(2019,12,31))
				df.to_csv(f'{path}{i}.csv')
			except KeyError:
				print(f'{i} was not pulled')
		else:
			print(f'{i} is already added')

def production_refresh(path):
	for i in config.tickers:
		if not (os.path.exists(f'{path}{i}{cd}.csv')):
			try:
				os.remove(f'{path}{i}{yd}.csv')
			except FileNotFoundError:
	#if you havent refreshed in a while check timedelta on yd before running.
	#could end up generating dupes if you're not careful
				print(f'{i}: no previous file found')
			try:
				df=pdr.get_data_yahoo(i,yr_ago,cd)
				config.prod_df_columns(df)
				df = df.tail(70)
				df.to_csv(f'{config.prod_SP_path}{i}{cd}.csv')
			except KeyError:
				print(f'{i} was not pulled')

		else:
			print(f'{i} is already added')


def production_refresh_SP500():
	path = config.prod_SP_path
	config.pull_SP_tickers()
	production_refresh(path)

def production_refresh_NASDAQ():
	path = config.prod_NASDAQ_path
	config.pull_NASDAQ_tickers()	
	production_refresh(path)

def uat_refresh_SP500():
	path = config.uat_SP_path
	config.pull_SP_tickers()
	uat_refresh(path)

def uat_refresh_NASDAQ():
	path = config.uat_NASDAQ_path
	config.pull_NASDAQ_tickers()	
	uat_refresh(path)

def production_refresh_full():
	config.pull_SP_tickers()
	production_refresh_SP500()
	config.tickers.clear()
	config.pull_NASDAQ_tickers()
	production_refresh_NASDAQ()

def uat_refresh_full():
	config.pull_SP_tickers()
	uat_refresh_SP500()
	config.tickers.clear()
	config.pull_NASDAQ_tickers()
	uat_refresh_NASDAQ()



