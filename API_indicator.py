import requests


#Define indicator
indicator = 'rsi'

endpoint = f'https://api.taapi.io/{indicator}'

secret = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjbHVlIjoiNjM2MTRiMzJmYzVhOGFkZmVjMTY1ZDM3IiwiaWF0IjoxNjY3MzIwNjI2LCJleHAiOjMzMTcxNzg0NjI2fQ.Hn9ah1yeZ2a80lpywFS_Wcp7Cmbsiuk6DbfMWqsJSSY'

parameters = {
    'secret': secret,
    'exchange': 'binance',
    'symbol': 'BTC/USDT',
    'interval': '5m',
    'backtracks': 20
}

response = requests.get(url = endpoint , params = parameters)

result = response.json()

print(result)