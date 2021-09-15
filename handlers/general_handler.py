from aiogram.dispatcher.webhook import SendMessage
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from datetime import date, time
import os,sys,inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 
from misc import dp, bot
import keyboards as kb

class TimezoneInfo(StatesGroup):
    current_user_time = State()

@dp.message_handler(commands=['start','menu'])
async def send_welcome(message: types.Message):
    if message.text == "/start":
        await message.reply( """Hi, I'm a bot reminder. I track changes in cryptocurrency prices and can constantly notify you about changes. 
                            There are two options. Constantly informing or informing when the price change for the chosen by you value (USD/USDT).""")
        #if check_register(message.from_user.id) == False:
        await message.reply("For start press /menu :D")
        #else:
            #await bot.send_message(message.from_user.id, "Але для початку потрібно вказати яка у вас година, нажміть на варіант ...")
            #await bot.send_message(message.from_user.id, send_time_text("string"))
            #await TimezoneInfo.current_user_time.set()###
    elif message.text == "/menu":
        await message.reply("Виберіть, що Вас цікавить.",reply_markup=kb.menu_markup())

#@dp.message_handler(state=TimezoneInfo.current_user_time, content_types=types.ContentTypes.TEXT)
#async def do_register(message: types.Message, state: FSMContext):
#    if message.text not in send_time_text("list"):
#        await message.reply("Будь ласка вибери годину зі списку")
#        return
#    await state.update_data(reminder_periodisity=message.text)
#    time_zone = calc_timezone(message.text[1:])
#    add_new_user(message.from_user.id, message.from_user.first_name, message.from_user.last_name, date.today(), message.from_user.language_code, time_zone )
#    await message.reply(f"Ваша часова зона {time_zone}.\nЖми /menu щоб продовжити.")
#    await state.finish()
