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

def update_currentces():
    currentces = cg.get_price(ids='bitcoin,litecoin,ethereum,xrp,cardano,tether,binancecoin,dogecoin,uniswap,chainlink,litecoin,tron,stellar,tezos,eos,miota,neo,dash,zcash', vs_currencies='usd')
    with open('currentces.json', 'w') as json_file:
        json.dump(currentces, json_file)


starttime=time.time()
while True:
    currentces = cg.get_price(ids='bitcoin,litecoin,ethereum,xrp,cardano,tether,binancecoin,dogecoin,uniswap,chainlink,litecoin,tron,stellar,tezos,eos,miota,neo,dash,zcash', vs_currencies='usd')
    with open('currentces.json', 'w') as json_file:
        json.dump(currentces, json_file)
    print(time_now())
    time.sleep(60.0 - ((time.time() - starttime) % 60.0))

