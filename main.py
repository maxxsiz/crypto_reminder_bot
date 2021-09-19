from aiogram import executor
from misc import dp
import handlers
import asyncio
from multiprocessing import Process
import json
import time 
from pycoingecko import CoinGeckoAPI
from api import time_now
from reminder_cheker import check_simple_reminders, check_db_reminders
        




def poling():
   print("Hello from poling Process")
   executor.start_polling(dp, skip_updates=True) 

def scrab():
   cg = CoinGeckoAPI()
   starttime=time.time()
   while True:
        currentces = cg.get_price(ids='bitcoin,litecoin,ethereum,xrp,cardano,tether,binancecoin,dogecoin,uniswap,chainlink,litecoin,tron,stellar,tezos,eos,miota,neo,dash,zcash', vs_currencies='usd')
        with open('currentces.json', 'w') as json_file:
            json.dump(currentces, json_file)
        print(time_now())
        check_simple_reminders()
        check_db_reminders()
        time.sleep(60.0 - ((time.time() - starttime) % 60.0))


if __name__ == "__main__":
   proc1 = Process(target=poling)
   proc2 = Process(target=scrab)
   proc1.start()
   proc2.start()
 
