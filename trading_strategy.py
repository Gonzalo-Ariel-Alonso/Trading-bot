ENTRY = abs(2.9)
VOLATILITY_SECURE = abs(ENTRY * 1.1)
STOP_LOSS = 1.1
TAKE_PROFIT = 4.4
FEES = 0.010
LEVERAGE = 2

class big_candle_strategy():
    def __init__(self):
        self.entry = ENTRY
        self.volatility_secure = abs(ENTRY * 1.1)
        self.stop_loss_percent = STOP_LOSS
        self.take_profit_percent = TAKE_PROFIT
        self.exchange_fees = FEES
        self.leverage = LEVERAGE

    def open_a_trade(self,h1_variation_percent,previus_trade_status):
        if abs(h1_variation_percent) >= ENTRY and previus_trade_status != 'Open' and abs(h1_variation_percent) < VOLATILITY_SECURE:
            open_a_trade = True
        else:
            open_a_trade = False
        return open_a_trade

    
    def take_profit_calculator(self,entry,position_type):
        if position_type == 'Long':
            take_profit = entry * (TAKE_PROFIT/100) + entry
        elif position_type == 'Short':
            take_profit = entry - entry * (TAKE_PROFIT/100)
        else:
            take_profit = 'ERROR'
        return take_profit   

    def stop_loss_calculator(self,entry,position_type):
        if position_type == 'Long':
            stop_loss = entry - entry * STOP_LOSS/100
        elif position_type == 'Short':
            stop_loss = entry * (STOP_LOSS/100) + entry
        else:
            stop_loss = 'ERROR'
        return stop_loss