import mysql.connector
import DB_targeted
import get_bybit
from datetime import datetime

candle_hisotry = DB_targeted.target()

cursor = candle_hisotry.cursor(buffered=True)


def insert_h1_candle(h1_response):
    for h1_candle in h1_response:
        timestamp = h1_candle['open_time']
        date_ = str(datetime.fromtimestamp(h1_candle['open_time']))[0:10]
        start_time = str(datetime.fromtimestamp(h1_candle['open_time']))[11:19]
        low = h1_candle['low']
        high = h1_candle['high']
        open_ = h1_candle['open']
        close_ = h1_candle['close']
        variation_percent = variation_percer(high,low,open_,close_)
        volume = h1_candle['volume']
        end_time = str(datetime.fromtimestamp(timestamp+3600))[11:19]
        sql_insert = 'INSERT INTO h1_candles(date_,start_time,\
        end_time,low,high,open_,close_,variation_percent,time_stamp,\
        volume) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        values = (date_, start_time, end_time, low, high, open_,close_,variation_percent, timestamp,volume)

        cursor.execute(sql_insert,values)

def insert_m5_candle(m5_response):
    h1_timestamp = m5_response[0]['open_time']
    h1_time = None
    start_time = 'hh:mm:ss'
    for m5_candle in m5_response:
        timestamp = m5_candle['open_time']
        date_ = str(datetime.fromtimestamp(m5_candle['open_time']))[0:10]
        start_time = str(datetime.fromtimestamp(m5_candle['open_time']))[11:19]
        h1_timestamp = h1_change(start_time,h1_time,h1_timestamp)
        h1_time = start_time[1] # Index 1 stand for hour index change
        low = m5_candle['low']
        high = m5_candle['high']
        open_ = m5_candle['open']
        close_ = m5_candle['close']
        variation_percent = variation_percer(high,low,open_,close_)
        volume = m5_candle['volume']
        end_time = str(datetime.fromtimestamp(timestamp+300))[11:19]

        sql_insert = 'INSERT INTO m5_candles(date_,start_time,\
        end_time,low,high,open_,close_,variation_percent,time_stamp,\
        volume,h1_time_stamp) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        values = (date_, start_time, end_time, low, high, open_,close_,variation_percent, timestamp,volume, h1_timestamp)
  
        cursor.execute(sql_insert,values)

    
def h1_change(start_time,h1_time,h1_timestamp):
    if start_time[1] == h1_time or h1_time == None:
        return h1_timestamp
    else:
        return h1_timestamp + 3600


def variation_percer(high,low,open,close):
    variation_percent = high / low * 100 - 100
    if open < close:
        variation_percent *= -1
    return variation_percent

def insert_candles():
    timestamp = 1662001200
    for i in range(0,60):
        response = get_bybit.response(timestamp,60,12)   
        insert_h1_candle(response)

        response = get_bybit.response(timestamp,5,144)
        insert_m5_candle(response)

        timestamp += 12 * 3600
        print('12 hours of cancles added succesfully')
        
    candle_hisotry.commit()
    return print("All Candles inserted succsefully")

insert_candles()