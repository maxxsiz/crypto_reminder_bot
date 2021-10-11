from aiogram import types
import os,sys,inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 
from misc import dp, bot
import keyboards as kb

@dp.message_handler(commands=['start','menu'])
async def send_welcome(message: types.Message):
    if message.text == "/start":
        await message.reply( """Hi, I'm a bot reminder. I track changes in cryptocurrency prices and can constantly notify you about changes.\n
        There are two options. Constantly informing or informing when the price change for the chosen by you value at USD.\n
        For start press /menu .""")
    elif message.text == "/menu":
        await message.reply("Choose, what you want.",reply_markup=kb.menu_markup())

