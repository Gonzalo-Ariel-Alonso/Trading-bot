import DB_targeted

candle_hisotry = DB_targeted.target()

cursor = candle_hisotry.cursor(buffered=True)

def insert_h1(date,start_time,end_time,low,high,open,close,variation_percent,timestamp,volume,h1_timestamp):
    sql_insert = 'INSERT INTO m5_candles(date_,start_time,\
    end_time,low,high,open_,close_,variation_percent,time_stamp,\
    volume,h1_time_stamp) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    values = (date, start_time, end_time, low, high, open,close,variation_percent,timestamp,volume, h1_timestamp)

    cursor.execute(sql_insert,values)

def commit_changes():
    candle_hisotry.commit()