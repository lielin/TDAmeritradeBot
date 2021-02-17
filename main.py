# Allows app to send HTTP request using python
import requests

# String that represents API KEY
key = '8ZQFGWTUEHSHIPYXG9THFNOBCESYYTKT'

# Get price history from market
def get_price_history(**kwargs):
    url = 'https://api.tdameritrade.com/v1/marketdata/{}/pricehistory'.format(kwargs.get('symbol'))

    params = {}
    params.update({'apikey': key})

    # Obtaining the args key and value
    for arg in kwargs:
        parameter = {arg: kwargs.get(arg)}
        # Updates parameters
        params.update(parameter)

    return requests.get(url, params=params).json()


# Prints stock data throughout day in minute intervals
print(get_price_history(symbol='AMZN', period=1, periodType='day', frequencyType='minute'))
