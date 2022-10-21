import DB_targeted
import json

"""This file will take the data from BTC_candle_hisotory data
base and its going to test the results of strategy descripted
in strategy.md"""


ENTRY = abs(2.5)
STOP_LOSS = 1.2
TAKE_PROFIT = 2.4

candle_hisotry = DB_targeted.target()

cursor = candle_hisotry.cursor(buffered=True)

def strategy_test():
    timestamp = str(1662001200)
    sql_consult = 'SELECT * FROM m5_candles'
    value = timestamp
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
        
        variation_sum += a_row[7]
        if abs(variation_sum) >= ENTRY and trade_record[-1]['Status'] != 'Open':
            add_trade(a_row[5],a_row[0],a_row[1],variation_sum,trade_record)
            variation_sum = 0 
        if trade_record and trade_record[-1]['Status'] == 'Open':
            trade_monitor(a_row[3],a_row[4],trade_record)

        if candle_count >= 12:
            candle_count = 0
            variation_sum = 0 
        
        candle_count += 1
        a_row = cursor.fetchone()
    strategy_results(trade_record)
   # trade_record_json(trade_record)



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
        for a_trade in trade_record:
            print('ID:',a_trade['ID'],'Status:',a_trade['Status'])
            for info in a_trade:
                a_trade[info] = str(a_trade[info])
            json.dump(a_trade, trade_record_json)

def strategy_results(trade_record):
    wins = loses = final_results = 0
    for a_trade in trade_record:
        print('ID:',a_trade['ID'],'Status:',a_trade['Status'])
        if a_trade['Status'] == 'Win':
            wins += 1
        elif a_trade['Status'] == 'Lose':
            loses += 1
    print('It tested a total of',len(trade_record),'trades in the period of time 30 days.')
    print('The result was:',wins,'wins and:',loses,'loses')

strategy_test()

    