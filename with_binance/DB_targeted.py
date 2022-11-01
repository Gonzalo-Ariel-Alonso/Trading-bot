import mysql.connector

def target():
    "Fill each variable with your data base information"
    database = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        password = '1234',
        database = 'binance_BTC_kline'
    )
    return database

target()