import requests

# API KEY for app
key = '8ZQFGWTUEHSHIPYXG9THFNOBCESYYTKT'


def get_price_history(**kwargs):
    url = 'https://api.tdameritrade.com/v1/marketdata/{}/pricehistory'.format(kwargs.get('symbol'))

    params = {}
    params.update({'apikey': key})

    for arg in kwargs:
        parameter = {arg: kwargs.get(arg)}
        params.update(parameter)

    return requests.get(url, params=params).json()


# Prints price of symbol per minute throughout the day
print(get_price_history(symbol='AMZN', period=1, periodType='day', frequencyType='minute'))
