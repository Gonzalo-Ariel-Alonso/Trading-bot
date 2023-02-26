import get_binance
def initial_conf():
    get_binance.log_in()
    get_binance.CLIENT.futures_change_leverage(symbol = 'BTCUSDT',leverage = 1)
    get_binance.CLIENT.futures_change_margin_type(symbol = 'BTCUSDT',marginype = 'ISOLATED')

def open_limit_position(side,quiantity,price):
    position_param = {
        'symbol':'BTCUSDT',
        'side':side,
        'type':'LIMIT',
        'timeInForce':get_binance.CLIENT.TIME_IN_FORCE_GTC,
        'quantity':quiantity,
        'price':price
    }

def stop_loss_order(side,stop_price):
    stop_loss_params = {
        'symbol':'BTCUSDT',
        'side':side,
        'type':'STOP_MARKET',
        'stopPrice':stop_price,
        'closePosition':True      
    }

def take_profit_order(side,stop_price,quiantity):
    take_profit_params = {
        'symbol':'BTCUSDT',
        'side':side,
        'type':get_binance.CLIENT.ORDER_TYPE_TAKE_PROFIT_LIMIT,
        'stopPrice':stop_price,
        'price': stop_price,
        'quiantity':quiantity, 

    }