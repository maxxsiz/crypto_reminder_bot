from pycoingecko import CoinGeckoAPI
import time
import json

cg = CoinGeckoAPI()

def get_price(coin):
    with open('currentces.json') as f:
        data = json.load(f)
    return data[coin]['usd']

def time_now():
    localtime = time.localtime()
    result = time.strftime("%I:%M:%S %p", localtime)
    return result 

def get_coin_list():
    with open('currentces.json') as f:
        data = json.load(f)
    return data

def get_coin_list_for_send():
    with open('currentces.json') as f:
        data = json.load(f)
    text = ''
    for i in data:
        text += "".format(data) 

    return data


