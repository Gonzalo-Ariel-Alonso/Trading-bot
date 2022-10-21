from re import S
from sqlite3 import Date
from pybit import usdt_perpetual
import pandas as pd
import time
from datetime import datetime

date = time.mktime(time.strptime('2022-10-03 21:00:00', '%Y-%m-%d %H:%M:%S'))

session_unauth = usdt_perpetual.HTTP(
    endpoint="https://api-testnet.bybit.com"
)
def response(timestamp_target,_interval,amount_of_results):
    "_interval goes on minutes"
    response = session_unauth.query_kline(
        symbol="BTCUSDT",
        interval=_interval,
        limit=amount_of_results,
        from_time=timestamp_target)
    return response['result']



