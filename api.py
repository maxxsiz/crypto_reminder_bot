from pycoingecko import CoinGeckoAPI
import datetime
import json

cg = CoinGeckoAPI()

def get_price(coin):
    with open('currentces.json') as f:
        data = json.load(f)
    return data[coin]['usd']
    
def get_price_all():
    with open('currentces.json') as f:
        data = json.load(f)
    return data

def time_now():
    now = datetime.datetime.now()
    result = now.strftime("%d-%m-%Y %H:%M")
    return result 

def get_coin_list():
    with open('currentces.json') as f:
        data = json.load(f)
    coin_list = data.keys()
    return coin_list

def get_coin_list_for_send():
    with open('currentces.json') as f:
        data = json.load(f)
    text = ''
    for key, val in data.items():
        text += "\n/{} | {} USD".format(key, val['usd']) 
    return text

