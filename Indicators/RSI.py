RSI_LENGTH = 14
candle_array = []
def RS_calculator(candle_array):
    positive_var_sum = negative_var_sum = 0
    count_negative = count_positive = 0
    if not len(candle_array) == RSI_LENGTH:
        return 'Length Error'
    else:
        for candle in candle_array:
            if candle['Variation'] > 0:
                positive_var_sum += candle['Variation']
                count_positive += 1
            else:
                negative_var_sum += candle['Variation']
                count_negative += 1
        positive_avg = positive_var_sum / count_positive
        negative_avg = negative_var_sum / count_negative
        RS = abs(positive_avg) / abs(negative_avg)
    return RS

def RSI_calculator(RS):
    RSI = 1 - 1 / (1+RS)
    return RSI

def candle_array_constructor(high,low,open,close):
    a_candle = {
        'High':high,
        'Low':low,
        'Open':open,
        'Close':close,
        'Variation': variation_calculator(close)
    }
    if len(candle_array) <= RSI_LENGTH:
        candle_array.append(a_candle)
    else:
        candle_array.pop(0)
        candle_array.append(a_candle)
    return candle_array

def variation_calculator(actual_close):
    if not candle_array:
        return 0
    else:
        previus_close = candle_array[-1]['Close']
        variation = actual_close - previus_close
        return variation