from aiogram import executor
from misc import dp
import asyncio
import aioschedule
import json
import time 
from pycoingecko import CoinGeckoAPI

cg = CoinGeckoAPI()

async def do_check():
    print("It's noon!")

async def scheduler():
    starttime = time.time()
    while True:
        with open('currentces.json', 'w') as json_file:
            json.dump(cg.get_price(ids='bitcoin,litecoin,ethereum,xrp,cardano,tether,binancecoin,dogecoin,uniswap,chainlink,litecoin,tron,stellar,tezos,eos,miota,neo,dash,zcash', vs_currencies='usd'), json_file)
        time.sleep(60.0 - ((time.time() - starttime) % 60.0))

async def on_startup(_):
    asyncio.create_task(scheduler())

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
