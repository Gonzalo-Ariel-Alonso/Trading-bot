from binance import *
import binance_conf
from datetime import datetime
import variation_percent_calc
import fill_DB


def log_in():
	client = Client(binance_conf.API_KEY,binance_conf.SECURITY_KEY)
	print('logged in')
	return client

"""kline format:
[
    [
      1499040000000,      // Kline open time
      "0.01634790",       // Open price
      "0.80000000",       // High price
      "0.01575800",       // Low price
      "0.01577100",       // Close price
      "148976.11427815",  // Volume
      1499644799999,      // Kline Close time
      "2434.19055334",    // Quote asset volume
      308,                // Number of trades
      "1756.87402397",    // Taker buy base asset volume
      "28.46694368",      // Taker buy quote asset volume
      "0"                 // Unused field, ignore.
    ]
    #repeat#
]"""


def send_kline_data(klines):
	m5_candles_in_h1 = 1
	hours_added = 0
	for a_candle in klines:

		timestamp = a_candle[0]/1000
		date = str(datetime.fromtimestamp(a_candle[0]/1000))[0:10]
		start_time = str(datetime.fromtimestamp(a_candle[0]/1000))[11:19]
		open = float(a_candle[1])
		high = float(a_candle[2])
		low = float(a_candle[3])
		close = float(a_candle[4])
		volume = float(a_candle[5])
		end_time = str(datetime.fromtimestamp(a_candle[6]/1000))[11:19]
		variation_percent = variation_percent_calc.variation_percent_calc(low,high,open,close,m5_candles_in_h1)
		if m5_candles_in_h1 == 1:
			h1_timestamp = timestamp
			hours_added += 1
		m5_candles_in_h1 = 1 if m5_candles_in_h1 >= 12 else m5_candles_in_h1+1
		fill_DB.insert_m5(date,start_time,end_time,low,high,open,close,variation_percent,timestamp,volume,h1_timestamp)
		if hours_added % 12 == 0:
			print('12 hours of candles added succsesfuly')

def iterate_multiple_request():
	client = log_in()
	MAX_REQUEST = 999
	INITIAL_TIMESTAMP = actual_timestamp = 1641006000000 # in miliseconds
	END_TIMESTAMP = 1667012400000
	MILISECONDS_IN_HOUR = 3600000
	while actual_timestamp < END_TIMESTAMP:
		end_request = actual_timestamp + MAX_REQUEST * MILISECONDS_IN_HOUR - 1
		#for futher documentation get inside of get_historical_klines
		klines = client.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_5MINUTE,actual_timestamp,end_request)
		send_kline_data(klines)
		actual_timestamp = end_request + 1
		print('999 candles added successfully')
	fill_DB.commit_changes()
