class big_candle_strategy:
    def __init__(self,
    ENTRY = abs(2.5),
    STOP_LOSS = 1.1,
    TAKE_PROFIT = 4.6,
    FEES = 0.010,
    LEVERAGE = 2):
        self.ENTRY = ENTRY
        self.VOLATILITY_SECURE = abs(ENTRY * 1.1) 
        self.STOP_LOSS_PERCENT = STOP_LOSS
        self.TAKE_PROFIT_PERCENT = TAKE_PROFIT
        self.EXCHANGE_FEES = FEES
        self.LEVERAGE = LEVERAGE

    def open_a_trade(self,h1_variation_percent,previus_trade_status):
        if abs(h1_variation_percent) >= self.ENTRY and previus_trade_status != 'Open' and abs(h1_variation_percent) < self.VOLATILITY_SECURE:
            open_a_trade = True
        else:
            open_a_trade = False
        return open_a_trade

    
    def take_profit_calculator(self,entry,position_type):
        if position_type == 'Long':
            take_profit = entry * (self.TAKE_PROFIT_PERCENT/100) + entry
        elif position_type == 'Short':
            take_profit = entry - entry * (self.TAKE_PROFIT_PERCENT/100)
        else:
            take_profit = 'ERROR'
        return take_profit   

    def stop_loss_calculator(self,entry,position_type):
        if position_type == 'Long':
            stop_loss = entry - entry * self.STOP_LOSS_PERCENT/100
        elif position_type == 'Short':
            stop_loss = entry * (self.STOP_LOSS_PERCENT/100) + entry
        else:
            stop_loss = 'ERROR'
        return stop_loss