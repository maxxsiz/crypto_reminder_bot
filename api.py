from pycoingecko import CoinGeckoAPI
import pandas as pd
import time
import numpy as np

cg = CoinGeckoAPI()
for i in range(20):
    localtime = time.localtime()
    result = time.strftime("%I:%M:%S %p", localtime)
    currentces = cg.get_price(ids='bitcoin,litecoin,ethereum', vs_currencies='tether')
    print(currentces)
    print(result)
    time.sleep(10)

##binance_data = cg.get_exchanges_by_id('binance')
#df_binance = pd.DataFrame(binance_data['tickers'], columns=['base','target','volume'])
#print(df_binance.head())