import csv

ticker_SP500path = '/Users/timothygould/Desktop/Python/Projects/Quant Trading/S&P500List.csv'
ticker_NASDAQpath ='/Users/timothygould/Desktop/Python/Projects/Quant Trading/NASDAQ.csv'
uat_SP_path = '/Users/timothygould/Google Drive/Quant Trading/Backtesting/Backtesting Data/UAT/S&P500/'
uat_NASDAQ_path = '/Users/timothygould/Google Drive/Quant Trading/Backtesting/Backtesting Data/UAT/NASDAQ/'
prod_SP_path =  '/Users/timothygould/Google Drive/Quant Trading/Backtesting/Backtesting Data/Production/S&P500/'
prod_NASDAQ_path =  '/Users/timothygould/Google Drive/Quant Trading/Backtesting/Backtesting Data/Production/NASDAQ/'
global tickers
tickers = []




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

#add df.iloc[] # to end of each row for reference
def uat_df_columns(df):
	#Moving Averages
			df['200MA'] = df.iloc[:,5].rolling(window=200).mean()#6
			df['150MA'] = df.iloc[:,5].rolling(window=150).mean()#7
			df['100MA'] = df.iloc[:,5].rolling(window=100).mean()#8
			df['75MA'] = df.iloc[:,5].rolling(window=75).mean()#9
			df['50MA'] = df.iloc[:,5].rolling(window=50).mean()#10
			df['35MA'] = df.iloc[:,5].rolling(window=35).mean()#11
			df['25MA'] = df.iloc[:,5].rolling(window=25).mean()#12
			df['15MA'] = df.iloc[:,5].rolling(window=15).mean()#13
			df['10MA'] = df.iloc[:,5].rolling(window=10).mean()#14

			#MACD
			df['ShortEMA'] = df.iloc[:,5].ewm(span=12,adjust=False).mean()#15
			df['LongEMA'] = df.iloc[:,5].ewm(span=26,adjust=False).mean()#16
			df['MACD'] = df['ShortEMA']-df['LongEMA']#17
			df['Signal'] = df['MACD'].ewm(span=9,adjust=False).mean()#18
			df['MACDdiff'] = round(df.iloc[:,17]-df.iloc[:,18],5)#19
			df['MACD-5D'] = df.iloc[:,17].shift(5)#20
			df['Signal-5D'] = df.iloc[:,18].shift(5)#21
			df['MACD-5Ddiff'] = round(df.iloc[:,20]-df.iloc[:,21],5)#22
			df['MACD-10D'] = df.iloc[:,17].shift(10)#23
			df['Signal-10D'] = df.iloc[:,18].shift(10)#24
			df['MACD-10Ddiff'] = round(df.iloc[:,23]-df.iloc[:,24],5)#25

			#RSI
			delta = df.iloc[:,5].diff(1)
			up = delta.copy()
			down = delta.copy()
			up[up<0] = 0
			down[down>0] = 0
			df['50avg_gain'] = up.rolling(window = 50).mean()
			df['50avg_loss'] = abs(down.rolling(window = 50).mean())
			RS = df.iloc[:,26]/df.iloc[:,27]
			RSI = 100 - (100/(1+RS))
			df['50RSI'] = 100 - (100/(1+(df.iloc[:,26]/df.iloc[:,27])))

			df['40avg_gain'] = up.rolling(window = 40).mean()
			df['40avg_loss'] = abs(down.rolling(window = 40).mean())
			RS = df.iloc[:,29]/df.iloc[:,30]
			RSI = 100 - (100/(1+RS))
			df['40RSI'] = 100 - (100/(1+(df.iloc[:,29]/df.iloc[:,30])))

			df['30avg_gain'] = up.rolling(window = 30).mean()
			df['30avg_loss'] = abs(down.rolling(window = 30).mean())
			RS = df.iloc[:,32]/df.iloc[:,33]
			RSI = 100 - (100/(1+RS))
			df['30RSI'] = 100 - (100/(1+(df.iloc[:,32]/df.iloc[:,33])))

			df['20avg_gain'] = up.rolling(window = 20).mean()
			df['20avg_loss'] = abs(down.rolling(window = 20).mean())
			RS = df.iloc[:,35]/df.iloc[:,36]
			RSI = 100 - (100/(1+RS))
			df['20RSI'] = 100 - (100/(1+(df.iloc[:,35]/df.iloc[:,36])))

			return df
def prod_df_columns(df):
	#Moving Averages
			df['200MA'] = df.iloc[:,5].rolling(window=200).mean()#6
			df['150MA'] = df.iloc[:,5].rolling(window=150).mean()#7
			df['100MA'] = df.iloc[:,5].rolling(window=100).mean()#8
			df['75MA'] = df.iloc[:,5].rolling(window=75).mean()#9
			df['50MA'] = df.iloc[:,5].rolling(window=50).mean()#10
			df['35MA'] = df.iloc[:,5].rolling(window=35).mean()#11
			df['25MA'] = df.iloc[:,5].rolling(window=25).mean()#12
			df['15MA'] = df.iloc[:,5].rolling(window=15).mean()#13
			df['10MA'] = df.iloc[:,5].rolling(window=10).mean()#14

			#MACD
			df['ShortEMA'] = df.iloc[:,5].ewm(span=12,adjust=False).mean()#15
			df['LongEMA'] = df.iloc[:,5].ewm(span=26,adjust=False).mean()#16
			df['MACD'] = df['ShortEMA']-df['LongEMA']#17
			df['Signal'] = df['MACD'].ewm(span=9,adjust=False).mean()#18
			df['MACDdiff'] = round(df.iloc[:,17]-df.iloc[:,18],5)#19
			df['MACD-5D'] = df.iloc[:,17].shift(5)#20
			df['Signal-5D'] = df.iloc[:,18].shift(5)#21
			df['MACD-5Ddiff'] = round(df.iloc[:,20]-df.iloc[:,21],5)#22
			df['MACD-10D'] = df.iloc[:,17].shift(10)#23
			df['Signal-10D'] = df.iloc[:,18].shift(10)#24
			df['MACD-10Ddiff'] = round(df.iloc[:,23]-df.iloc[:,24],5)#25

			#RSI
			delta = df.iloc[:,5].diff(1)
			up = delta.copy()
			down = delta.copy()
			up[up<0] = 0
			down[down>0] = 0
			df['50avg_gain'] = up.rolling(window = 50).mean()
			df['50avg_loss'] = abs(down.rolling(window = 50).mean())
			RS = df.iloc[:,26]/df.iloc[:,27]
			RSI = 100 - (100/(1+RS))
			df['50RSI'] = 100 - (100/(1+(df.iloc[:,26]/df.iloc[:,27])))

			df['40avg_gain'] = up.rolling(window = 40).mean()
			df['40avg_loss'] = abs(down.rolling(window = 40).mean())
			RS = df.iloc[:,29]/df.iloc[:,30]
			RSI = 100 - (100/(1+RS))
			df['40RSI'] = 100 - (100/(1+(df.iloc[:,29]/df.iloc[:,30])))

			df['30avg_gain'] = up.rolling(window = 30).mean()
			df['30avg_loss'] = abs(down.rolling(window = 30).mean())
			RS = df.iloc[:,32]/df.iloc[:,33]
			RSI = 100 - (100/(1+RS))
			df['30RSI'] = 100 - (100/(1+(df.iloc[:,32]/df.iloc[:,33])))

			df['20avg_gain'] = up.rolling(window = 20).mean()
			df['20avg_loss'] = abs(down.rolling(window = 20).mean())
			RS = df.iloc[:,35]/df.iloc[:,36]
			RSI = 100 - (100/(1+RS))
			df['20RSI'] = 100 - (100/(1+(df.iloc[:,35]/df.iloc[:,36])))

			return df

			