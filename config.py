import csv
from sqlalchemy import create_engine
import psycopg2

ticker_SP500path = '/Users/timothygould/Desktop/Python/Projects/Quant Trading/S&P500List.csv'
ticker_NASDAQpath ='/Users/timothygould/Desktop/Python/Projects/Quant Trading/NASDAQ.csv'
global tickers
tickers = []

localpwd = 'pwd'
localengine = create_engine(f'postgresql://postgres:{localpwd}@localhost/tradedatatest')
serverengine = create_engine(f'postgresql://sysadmin:Sysadmin123@database-1.c9zekcxdkpeh.us-east-2.rds.amazonaws.com:5375/quantframework')

def pull_SP_tickers():
	with open (ticker_SP500path) as csv_file:
		reader = csv.reader(csv_file)
		for row in reader:
			tickers.append(row[0])
			
def pull_NASDAQ_tickers():
	with open (ticker_NASDAQpath) as csv_file:
		reader = csv.reader(csv_file)
		for row in reader:
			tickers.append(row[0])

def rename_df_columns(df):
	df.rename(columns = 
	{'Date':'date',
	'High':'high',
	'Low':'low',
	'Open':'open',
	'Close':'close',
	'Volume':'volume',
	'Adj Close':'adj_close'},
	inplace=True)
	return df


	