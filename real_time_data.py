import get_binance
import schedule
import time
import get_binance
from binance import *
from datetime import datetime
import fill_DB

def get_price():
    info = get_binance.client.get_margin_price_index(symbol='BTCUSDT')
    return print(info)

def get_real_time_price():
    schedule.every(1).seconds.do(get_price)
    while 1:
        schedule.run_pending()
        time.sleep(1)

def get_last_5m_candle():
    client = get_binance.log_in()
    now_timestamp = int(round(time.time(),0))
    last_m5_timestamp_completed = now_timestamp - now_timestamp%300 - 300
    last_m5_candle = client.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_5MINUTE,last_m5_timestamp_completed*1000,(last_m5_timestamp_completed+299)*1000)
    return last_m5_candle

def fill_data_base_real_time():
    fill_data_base()
    schedule.every(301).seconds.do(fill_data_base)
    while 1:
        schedule.run_pending()
        time.sleep(301)

def fill_data_base():
    last_5m_candle = get_last_5m_candle()
    get_binance.send_kline_data(last_5m_candle)
    print('5 mins candle added succsessfully')
    fill_DB.commit_changes()

def prof_of_runing():
    schedule.every(30).seconds.do(runing)
    while 1:
        schedule.run_pending()
        time.sleep(30)

def runing():
    print('Runing..')

def open_position(type):
    if type == 'Short':
        asd = 2


def futures_account_balance():
    get_binance.log_in()
    futures_balance = get_binance.CLIENT.futures_account_balance()
    return futures_balance

print(futures_account_balance())