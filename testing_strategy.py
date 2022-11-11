import DB_targeted
import json
import trading_strategy
import Candle



def run_strategy(strategy,comentaries = True):
    "Run strategy and save trade all trades info in a dictionaries"
    #Conection to data base
    candle_hisotry = DB_targeted.target()
    cursor = candle_hisotry.cursor(buffered=True)

    #SQL querys
    sql_consult = 'SELECT * FROM m5_candles'
    cursor.execute(sql_consult)

    candle_count = 0
    trade_record = [{'ID':None,'Status':'Record_initialization'}]

    a_row = cursor.fetchone()
    #Row structure:
    # Date = a_row[0] , Start time = a_row[1], End time = a_row[2]
    # Low = a_row[3] , High = a_row[4] , Open = a_row[5] , Close = a_row[6]
    # Variation = a_row[7],timestamp = a_row[8] , Volume = a_row[9]

    while a_row:
        a_candle = Candle.m5_Candle(a_row[0],a_row[1],a_row[2],a_row[3],a_row[4],a_row[5],a_row[6],a_row[7],a_row[8],a_row[9],a_row[10])
        variation_sum = a_candle.h1_variation

        # Condition to open a trade
        if strategy.open_a_trade(variation_sum,trade_record[-1]['Status']):
            entry_price = a_candle.close
            entry_date = a_candle.date
            entry_time = a_candle.end_time
            add_trade(entry_price,entry_date,entry_time,variation_sum,trade_record,strategy)
            variation_sum = 0 
        
        # If there is a trade open, track his performance
        if trade_record[-1]['Status'] == 'Open':
            trade_monitor(a_row[0],a_row[2],a_row[4],a_row[3],trade_record)
        
        # Resert candle count every hour (5 min * 12 = 1 hour)
        if candle_count >= 12:
            candle_count = 1
            variation_sum = 0 
        else:
            candle_count += 1
        #Next row
        a_row = cursor.fetchone()

    #Remove trade_record initialization
    trade_record.pop(0)

    return trade_record
    #trade_record_json(trade_record)



def trade_monitor(end_date,end_time,high,low,trade_record):
    stop_loss = trade_record[-1]['Stop loss']
    take_profit = trade_record[-1]['Take profit']
    position_type = trade_record[-1]['Type']

    #Long operation
    if position_type == 'Long':
        if high > take_profit:
            trade_record[-1]['Status'] = 'Win' #Take profit reached
        elif low < stop_loss:
            trade_record[-1]['Status'] = 'Lose' #Stop loss reached

    #Short operation
    elif position_type == 'Short':
        if high > stop_loss:
            trade_record[-1]['Status'] = 'Lose' #Stop loss reached
        elif low < take_profit:
            trade_record[-1]['Status'] = 'Win' #Take profit reached
    
    #If trade is not open anymore, record exit date and time
    if trade_record[-1]['Status'] != 'Open':
        trade_record[-1]['Exit time'] = str(end_date)+' '+str(end_time)




def add_trade(entry,date,time,variation,trade_record,strategy):
    """List of dictionaries with all trade info"""
    position_type = 'Short' if variation < 0 else 'Long'
    trade_record.append({
        'ID': len(trade_record),
        'Date': date,
        'Time':time,
        'Type':position_type,
        'Entry':entry,
        'Stop loss': strategy.stop_loss_calculator(float(entry),position_type),
        'Take profit': strategy.take_profit_calculator(float(entry),position_type),
        'Status': 'Open',
        'Exit time':'Null'
    })
    

def trade_record_json(trade_record):
    with open(f'\\trade_record.json','w') as trade_record_json:
        for info in trade_record:
            trade_record[info] = trade_record[info]
        json.dump(trade_record, trade_record_json)

def strategy_results(trade_record,strategy,comentaries = True):
    """Test results based on trades recorded"""
    wins = loses = 0
    initial_money = 100
    actual_money = initial_money
    previus_month = '1'
    for a_trade in trade_record:
        if not comentaries:
            print('ID:',a_trade['ID'],'Date:',a_trade['Date'],a_trade['Time'],'Status:',a_trade['Status'])
        if a_trade['Status'] == 'Win':
            wins += 1
            actual_money = win_trade_rebalance(actual_money,strategy)
        elif a_trade['Status'] == 'Lose':
            loses += 1
            actual_money = lose_trade_rebalance(actual_money,strategy)
        if actual_money < 0:
            print('YOU GOT LIQUIDATED!!')
            break

        if previus_month != str(a_trade['Date'])[6]:
            print('Account perfonamnce in the month number',previus_month,'is:',account_perfomance(initial_money,actual_money))
            previus_month = str(a_trade['Date'])[6]
            actual_money = 100

    performance = account_perfomance(initial_money,actual_money)
    if comentaries:
        print('It tested a total of',len(trade_record),'trades in the period of time 296 days.')
        print('The result was:',wins,'wins and:',loses,'loses')
        print('From the initial ammount of $',initial_money,',now you have $',round(actual_money,2))
        print('The performance in your account was: %',performance)
        #analyce_a_trade(trade_record,117)
        
    return performance
    

def lose_trade_rebalance(actual_money,strategy):
    partial_loss = actual_money * (strategy.STOP_LOSS_PERCENT / 100) * strategy.LEVERAGE
    net_loss = partial_loss + partial_loss * strategy.EXCHANGE_FEES * strategy.LEVERAGE
    return actual_money - net_loss

def win_trade_rebalance(actual_money,strategy):
    partial_win = actual_money * (strategy.TAKE_PROFIT_PERCENT / 100) * strategy.LEVERAGE
    net_win = partial_win - partial_win * strategy.EXCHANGE_FEES * strategy.LEVERAGE
    return actual_money + net_win

def account_perfomance(initial_money,actual_money):
    perfomance = (actual_money/initial_money*100)-100
    return round(perfomance,2)

def test_strategy_with_multiples_variables():
    best_performance = {
        'Entry': 0,
        'Stop loss': 0,
        'Take profit': 0,
        'Performance %': -100
    }
    for entry in range (22,33,1):
        ENTRY = abs(entry / 10)
        print('Testing with entry of %',ENTRY)
        for sl in range(4,13,1):
            STOP_LOSS = sl / 10
            print('testing with stop loss of %',STOP_LOSS)
            for tp in range(36,53,2):
                TAKE_PROFIT = tp / 10
                strategy = trading_strategy.big_candle_strategy(ENTRY,STOP_LOSS,TAKE_PROFIT)
                trade_record = run_strategy(strategy,comentaries = False)
                performance = strategy_results(trade_record,strategy,comentaries = False)
                if performance > best_performance['Performance %']:
                    best_performance['Entry'] = strategy.ENTRY
                    best_performance['Stop loss'] = strategy.STOP_LOSS_PERCENT
                    best_performance['Take profit'] = strategy.TAKE_PROFIT_PERCENT
                    best_performance['Performance %'] = performance
                    print('New best performance:',best_performance)
                    trade_record_json(best_performance)
    print(best_performance)

def analyce_a_trade(trade_list,trade_id):

    print('ID',trade_list[trade_id]['ID'])
    print('Entry',trade_list[trade_id]['Entry'])
    print('Stop loss',trade_list[trade_id]['Stop loss'])
    print('Take profit',trade_list[trade_id]['Take profit'])
    print('Exit time',trade_list[trade_id]['Exit time'])


def test_strategy():
    big_candle_strategy = trading_strategy.big_candle_strategy()
    trade_record = run_strategy(big_candle_strategy)
    strategy_results(trade_record,big_candle_strategy,comentaries = True)
