import mysql.connector
import DB_targeted
import get_bybit
from datetime import datetime

candle_hisotry = DB_targeted.target()

cursor = candle_hisotry.cursor(buffered=True)

H1_HIGH = 0
H1_LOW = 1000000
H1_OPEN = 0


def insert_h1_candle(h1_response):
    for h1_candle in h1_response:
        timestamp = h1_candle['open_time']
        date_ = str(datetime.fromtimestamp(h1_candle['open_time']))[0:10]
        start_time = str(datetime.fromtimestamp(h1_candle['open_time']))[11:19]
        low = h1_candle['low']
        high = h1_candle['high']
        open_ = h1_candle['open']
        close_ = h1_candle['close']
        variation_percent = 0 #variation_percent_calc(high,low,open_,close_)
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
    m5_candles_in_h1 = 1
    for m5_candle in m5_response:
        timestamp = m5_candle['open_time']
        date_ = str(datetime.fromtimestamp(m5_candle['open_time']))[0:10]
        start_time = str(datetime.fromtimestamp(m5_candle['open_time']))[11:19]
        low = m5_candle['low']
        high = m5_candle['high']
        open_ = m5_candle['open']
        close_ = m5_candle['close']
        volume = m5_candle['volume']
        h1_timestamp = h1_change(start_time,h1_time,h1_timestamp)
        variation_percent = variation_percent_calc(low,high,open_,close_,m5_candles_in_h1)
        h1_time = start_time[1] # Index 1 stand for hour index change
        end_time = str(datetime.fromtimestamp(timestamp+300))[11:19]

        m5_candles_in_h1 = 1 if m5_candles_in_h1 >= 12 else m5_candles_in_h1+1
        
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


def variation_percent_calc(m5_low,m5_high,m5_open,m5_close,m5_candles_in_h1):
    global H1_LOW
    global H1_HIGH
    global H1_OPEN

    if m5_candles_in_h1 == 1:
        H1_OPEN = m5_open
        H1_HIGH = m5_high
        H1_LOW = m5_low
    else:
        if m5_high > H1_HIGH:
            H1_HIGH = m5_high        
        if m5_low < H1_LOW:
            H1_LOW = m5_low
    
    if H1_OPEN > m5_close:
        variation =  (H1_HIGH/H1_LOW *100 - 100) * -1
    else:
        variation =  H1_HIGH/H1_LOW *100 - 100
    return variation

        
def positive_variation_percent(hour_low,actual_high):
    """If positive variation percent return negative value price did go down"""
    return actual_high / hour_low * 100 - 100

def negative_variation_percent(hour_high,actual_low):
    """If negative variation percent return positive value price did go up"""
    return actual_low / hour_high * 100 - 100


def insert_candles():
    timestamp = 1641006000
    days_of_info = 297
    candles_per_request = 12
    M5_CANDLES_IN_H1 = 12   
    SECONDS_IN_HOURS = 3600
    for i in range(0,days_of_info * 2):
        interval_in_minutes = 60
        by_bit_response = get_bybit.response(timestamp,interval_in_minutes,candles_per_request)   
        insert_h1_candle(by_bit_response)

        interval_in_minutes = 5
        by_bit_response = get_bybit.response(timestamp,interval_in_minutes,candles_per_request * M5_CANDLES_IN_H1)
        insert_m5_candle(by_bit_response)

        timestamp += candles_per_request * SECONDS_IN_HOURS
        print('12 hours of cancles added succesfully')
        
    candle_hisotry.commit()
    return print("All Candles inserted succsefully")

insert_candles()