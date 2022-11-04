
H1_HIGH = 0
H1_LOW = 1000000
H1_OPEN = 0

def variation_percent_calc(m5_low,m5_high,m5_open,m5_close,m5_candles_in_h1):
    global H1_LOW
    global H1_HIGH
    global H1_OPEN

    if m5_candles_in_h1 == 1:
        H1_OPEN = m5_open
        H1_HIGH = m5_high
        H1_LOW = m5_low
    else:
        if m5_high > H1_HIGH:
            H1_HIGH = m5_high        
        if m5_low < H1_LOW:
            H1_LOW = m5_low
    
    if H1_OPEN > m5_close:
        variation =  (H1_HIGH/H1_LOW *100 - 100) * -1
    else:
        variation =  H1_HIGH/H1_LOW *100 - 100
    return variation