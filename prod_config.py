
import pandas as pd
#broken up into 3 sections
##Buy chunks
##Sell chunks
##Prod dataframe/database columns

def buy_criteria_v2(df,buysearch):
	n=buysearch
	RSI_Lookback = []
	if df['ma35'][n]<df['ma50'][n] and df['ma35'][n-1]>df['ma50'][n-1]:
		pass
		if df['macd_10diff'][n]<df['macd_5diff'][n]<df['macd_diff'][n]:
			return True

def sell_criteria_v1(df,sellsearch):
	n2 = sellsearch
	if df['ma15'][n2]>df['ma35'][n2] and df['ma15'][n2-1]<df['ma35'][n2-1]:
		return True
def grab_sql(ticker,engine):
	df = pd.read_sql_query(f'''
				SELECT 
				lv_daily_trade_data.date,
				lv_daily_trade_data.ticker,
				lv_daily_trade_data.adj_close,
				lv_macd.macd,
				lv_macd.signal,
				lv_macd.macd_diff,
				lv_macd.macd_5d,
				lv_macd.signal_5d,
				lv_macd.macd_5diff,
				lv_macd.macd_10d,
				lv_macd.signal_10d,
				lv_macd.macd_10diff,
				lv_moving_averages.ma200,
				lv_moving_averages.ma150,
				lv_moving_averages.ma100,
				lv_moving_averages.ma75,
				lv_moving_averages.ma50,
				lv_moving_averages.ma35,
				lv_moving_averages.ma25,
				lv_moving_averages.ma15,
				lv_moving_averages.ma10,
				lv_rsi.rsi50,
				lv_rsi.rsi40,
				lv_rsi.rsi30,
				lv_rsi.rsi20
				FROM
				lv_daily_trade_data
				JOIN lv_macd
				ON lv_daily_trade_data.date=lv_macd.date
				AND lv_daily_trade_data.ticker=lv_macd.ticker
				JOIN lv_moving_averages
				ON lv_daily_trade_data.date=lv_moving_averages.date
				AND lv_daily_trade_data.ticker=lv_moving_averages.ticker
				JOIN lv_rsi
				ON lv_daily_trade_data.date=lv_rsi.date
				AND lv_daily_trade_data.ticker=lv_rsi.ticker
				WHERE lv_daily_trade_data.ticker = '{ticker}'
				ORDER BY lv_daily_trade_data.date ASC''',engine)
	return df


def prod_df_columns(df,outstanding_shares):
	#Moving Averages
	df['ma200'] = df.iloc[:,5].rolling(window=200).mean()#6
	df['ma150'] = df.iloc[:,5].rolling(window=150).mean()#7
	df['ma100'] = df.iloc[:,5].rolling(window=100).mean()#8
	df['ma75'] = df.iloc[:,5].rolling(window=75).mean()#9
	df['ma50'] = df.iloc[:,5].rolling(window=50).mean()#10
	df['ma35'] = df.iloc[:,5].rolling(window=35).mean()#11
	df['ma25'] = df.iloc[:,5].rolling(window=25).mean()#12
	df['ma15'] = df.iloc[:,5].rolling(window=15).mean()#13
	df['ma10'] = df.iloc[:,5].rolling(window=10).mean()#14

	#MACD
	df['short_ema'] = df.iloc[:,5].ewm(span=12,adjust=False).mean()#15
	df['long_ema'] = df.iloc[:,5].ewm(span=26,adjust=False).mean()#16
	df['macd'] = df['short_ema']-df['long_ema']#17
	df['signal'] = df['macd'].ewm(span=9,adjust=False).mean()#18
	df['macd_diff'] = round(df.iloc[:,17]-df.iloc[:,18],5)#19
	df['macd_5d'] = df.iloc[:,17].shift(5)#20
	df['signal_5d'] = df.iloc[:,18].shift(5)#21
	df['macd_5diff'] = round(df.iloc[:,20]-df.iloc[:,21],5)#22
	df['macd_10d'] = df.iloc[:,17].shift(10)#23
	df['signal_10d'] = df.iloc[:,18].shift(10)#24
	df['macd_10diff'] = round(df.iloc[:,23]-df.iloc[:,24],5)#25

	#RSI
	delta = df.iloc[:,5].diff(1)
	up = delta.copy()
	down = delta.copy()
	up[up<0] = 0
	down[down>0] = 0
	df['avg_gain50'] = up.rolling(window = 50).mean()
	df['avg_loss50'] = abs(down.rolling(window = 50).mean())
	RS = df.iloc[:,26]/df.iloc[:,27]
	RSI = 100 - (100/(1+RS))
	df['rsi50'] = 100 - (100/(1+(df.iloc[:,26]/df.iloc[:,27])))

	df['avg_gain40'] = up.rolling(window = 40).mean()
	df['avg_loss40'] = abs(down.rolling(window = 40).mean())
	RS = df.iloc[:,29]/df.iloc[:,30]
	RSI = 100 - (100/(1+RS))
	df['rsi40'] = 100 - (100/(1+(df.iloc[:,29]/df.iloc[:,30])))

	df['avg_gain30'] = up.rolling(window = 30).mean()
	df['avg_loss30'] = abs(down.rolling(window = 30).mean())
	RS = df.iloc[:,32]/df.iloc[:,33]
	RSI = 100 - (100/(1+RS))
	df['rsi30'] = 100 - (100/(1+(df.iloc[:,32]/df.iloc[:,33])))

	df['avg_gain20'] = up.rolling(window = 20).mean()
	df['avg_loss20'] = abs(down.rolling(window = 20).mean())
	RS = df.iloc[:,35]/df.iloc[:,36]
	RSI = 100 - (100/(1+RS))
	df['rsi20'] = 100 - (100/(1+(df.iloc[:,35]/df.iloc[:,36])))

	df['mkt_cap'] = df.iloc[:,5]*int(outstanding_shares)

	return df


