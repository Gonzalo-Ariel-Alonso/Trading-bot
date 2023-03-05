import mysql.connector

def target():
    "Fill each variable with your data base information"
    database = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        password = '1234',
        database = 'btc_candle_history'
    )
    return database

target()