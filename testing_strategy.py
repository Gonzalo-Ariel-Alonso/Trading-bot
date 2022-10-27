import DB_targeted
import json

"""This file will take the data from BTC_candle_hisotory data
base and its going to test the results of strategy descripted
in strategy.md"""


ENTRY = abs(2.0)
VOLATILITY_SECURE = abs(ENTRY * 1.3)
STOP_LOSS = 0.2
TAKE_PROFIT = 2.4
FEES = 0.006
LEVERAGE = 1

candle_hisotry = DB_targeted.target()

cursor = candle_hisotry.cursor(buffered=True)

def strategy_test():
    sql_consult = 'SELECT * FROM m5_candles'
    cursor.execute(sql_consult)
    a_row = cursor.fetchone()
    
    #print('Date',a_row[0])
    #print('Start time',a_row[1])
    #print('End time',a_row[2])
    #print('Low',a_row[3])
    #print('High',a_row[4])
    #print('Open',a_row[5])
    #print('Close',a_row[6])
    #print('Variation',a_row[7])
    #print('h1 timestamp',a_row[8])
    #print('Volume',a_row[9])
    candle_count = 0
    variation_sum = 0
    trade_record = [{'ID':None,'Status':'Record_initialization'}]
    while a_row:
        
        variation_sum = a_row[7]
        if abs(variation_sum) >= ENTRY and trade_record[-1]['Status'] != 'Open' and abs(variation_sum) < VOLATILITY_SECURE:
            add_trade(a_row[5],a_row[0],a_row[1],variation_sum,trade_record)
            variation_sum = 0 
        if trade_record[-1]['Status'] == 'Open':
            trade_monitor(a_row[3],a_row[4],trade_record)

        if candle_count >= 12:
            candle_count = 0
            variation_sum = 0 
        
        candle_count += 1
        a_row = cursor.fetchone()
    trade_record.pop(0)
    return strategy_results(trade_record)
    #trade_record_json(trade_record)



def trade_monitor(high,low,trade_record):
    stop_loss = trade_record[-1]['Stop loss']
    take_profit = trade_record[-1]['Take profit']
    position_type = trade_record[-1]['Type']
    if position_type == 'Long':
        if high > take_profit:
            trade_record[-1]['Status'] = 'Win'
        elif low < stop_loss:
            trade_record[-1]['Status'] = 'Lose'
    elif position_type == 'Short':
        if high > stop_loss:
            trade_record[-1]['Status'] = 'Lose'
        elif low < take_profit:
            trade_record[-1]['Status'] = 'Win'




def add_trade(entry,date,time,variation,trade_record):
    position_type = 'Short' if variation < 0 else 'Long'
    trade_record.append({
        'ID': len(trade_record),
        'Date': date,
        'Time':time,
        'Type':position_type,
        'Entry':entry,
        'Stop loss': stop_loss_calculator(float(entry),position_type),
        'Take profit': take_profit_calculator(float(entry),position_type),
        'Status': 'Open',
    })
    
def take_profit_calculator(entry,position_type):
    if position_type == 'Long':
        take_profit = entry * (TAKE_PROFIT/100) + entry
    elif position_type == 'Short':
        take_profit = entry - entry * (TAKE_PROFIT/100)
    else:
        take_profit = 'ERROR'
    return take_profit   

def stop_loss_calculator(entry,position_type):
    if position_type == 'Long':
        stop_loss = entry - entry * STOP_LOSS/100
    elif position_type == 'Short':
        stop_loss = entry * (STOP_LOSS/100) + entry
    else:
        stop_loss = 'ERROR'
    return stop_loss


def trade_record_json(trade_record):
    with open(f'\\trade_record.json','w') as trade_record_json:
        for info in trade_record:
            trade_record[info] = trade_record[info]
        json.dump(trade_record, trade_record_json)

def strategy_results(trade_record):
    global FEES
    global LEVERAGE
    wins = loses = 0
    initial_money = 100
    actual_money = initial_money
    for a_trade in trade_record:
        print('ID:',a_trade['ID'],'Date:',a_trade['Date'],a_trade['Time'],'Status:',a_trade['Status'])
        if a_trade['Status'] == 'Win':
            wins += 1
            actual_money = win_trade_formula(actual_money,FEES,LEVERAGE)
        elif a_trade['Status'] == 'Lose':
            loses += 1
            actual_money = lose_trade_formula(actual_money,FEES,LEVERAGE)
        if actual_money < 0:
            print('YOU GOT LIQUIDATED!!')
            break

    performance = account_perfomance(initial_money,actual_money)
    comentaries = True
    if comentaries:
        print('It tested a total of',len(trade_record),'trades in the period of time 296 days.')
        print('The result was:',wins,'wins and:',loses,'loses')
        print('From the initial ammount of $',initial_money,',now you have $',round(actual_money,2))
        print('The performance in your account was: %',performance)

    return performance
    

def lose_trade_formula(actual_money,fees,leverage):
    partial_loss = actual_money * (STOP_LOSS / 100) * leverage
    net_loss = partial_loss + partial_loss * fees * leverage
    return actual_money - net_loss

def win_trade_formula(actual_money,fees,leverage):
    partial_win = actual_money * (TAKE_PROFIT / 100) * leverage
    net_win = partial_win - partial_win * fees * leverage
    return actual_money + net_win

def account_perfomance(initial_money,actual_money):
    perfomance = (actual_money/initial_money*100)-100
    return round(perfomance,2)

def st_tp_test():
    global STOP_LOSS
    global TAKE_PROFIT
    global ENTRY
    best_performance = {
        'Entry': 0,
        'Stop loss': 0,
        'Take profit': 0,
        'Performance %': 0
    }
    for entry in range (20,25,1):
        ENTRY = abs(entry / 10)
        print('Testing with entry of %',ENTRY)
        for sl in range(2,13,2):
            STOP_LOSS = sl / 10
            print('testing with stop loss of %',STOP_LOSS)
            for tp in range(24,37,2):
                TAKE_PROFIT = tp / 10
                performance = strategy_test()
                if performance > best_performance['Performance %']:
                    best_performance['Entry'] = ENTRY
                    best_performance['Stop loss'] = STOP_LOSS
                    best_performance['Take profit'] = TAKE_PROFIT
                    best_performance['Performance %'] = performance
                    print('New best performance:',best_performance)
                    trade_record_json(best_performance)
    print(best_performance)

#st_tp_test()
strategy_test()

#TOP RESULT:
# {"Entry": 2.0, "Stop loss": 0.2, "Take profit": 2.4, "Performance %": 3964.38}
# {"Entry": 2.3, "Stop loss": 0.2, "Take profit": 2.6, "Performance %": 2498.29}
# {"Entry": 2.3, "Stop loss": 0.6, "Take profit": 2.0, "Performance %": 1219.12}