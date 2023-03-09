class m5_Candle:
    def __init__(self,date,start_time,end_time,low,high,open,close,h1_variation,timestamp,volume):
        self.date = date
        self.start_time = start_time
        self.end_time = end_time
        self.low = low
        self.high = high
        self.open = open
        self.close = close
        self.h1_variation = h1_variation
        self.timestamp = timestamp
        self.volume = volume
