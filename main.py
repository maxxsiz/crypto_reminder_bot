from aiogram import executor
from misc import dp
from multiprocessing import Process
import json
import time 
from pycoingecko import CoinGeckoAPI
from api import time_now
from reminder_checker import check_simple_reminders, check_db_reminders
import handlers


def poling(): #Start bot polling process
   print("Hello from poling Process")
   executor.start_polling(dp, skip_updates=True) 

def scrab(): #Start checking prices every 1 min
   cg = CoinGeckoAPI()
   starttime=time.time()
   while True:
      currentces = cg.get_price(ids='bitcoin,litecoin,ethereum,xrp,cardano,tether,binancecoin,dogecoin,uniswap,chainlink,litecoin,tron,stellar,tezos,eos,miota,neo,dash,zcash', vs_currencies='usd')
      with open('currentces.json', 'w') as json_file:  #update coins prices from CoinGecko.com
         json.dump(currentces, json_file)

      print(time_now()) #current time
      check_db_reminders() #function checking reminders with values 

      if time_now()[-2:] == "00":
         check_simple_reminders("1hour") #sending notification every 1 hour
         if time_now()[-5:] in ["00:00","03:00","06:00","09:00","12:00","15:00","18:00","21:00"]:
            check_simple_reminders("3hour") #sending notification every 3 hours
            if time_now()[-5:] in ["00:00","06:00","12:00","18:00"]:
               check_simple_reminders("6hour") #sending notification every 6 hours
            if time_now()[-5:] in ["09:00","21:00"]:
               check_simple_reminders("12hour") #sending notification twice a day at 09:00 and 21:00
            if time_now()[-5:] == "09:00": 
               check_simple_reminders("24hour") #sending notification every day at 09:00
      time.sleep(60.0 - ((time.time() - starttime) % 60.0))


if __name__ == "__main__":
   proc1 = Process(target=poling)
   proc2 = Process(target=scrab)
   proc1.start()
   proc2.start()
 
