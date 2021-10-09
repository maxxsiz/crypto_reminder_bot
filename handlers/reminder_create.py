from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 
from misc import dp, bot
from valid_func import check_coin_id, check_price_value
from db_func import add_reminder, get_new_id
from api import time_now, get_price, get_coin_list_for_send
import keyboards as kb

class ReminderInfo(StatesGroup):
    waiting_for_reminder_coin_id = State()
    waiting_for_reminder_periodisity = State()

 
@dp.callback_query_handler(lambda c: c.data == "add_reminder_simple", state = "*")
async def add_reminder_callback(callback_query: types.CallbackQuery):
    chat_id = callback_query.from_user.id
    await bot.delete_message(chat_id, callback_query.message.message_id)
    coin_list = get_coin_list_for_send()
    await bot.send_message(chat_id, "Choose coin." + coin_list)
    await ReminderInfo.waiting_for_reminder_coin_id.set()

@dp.message_handler(state=ReminderInfo.waiting_for_reminder_coin_id, content_types=types.ContentTypes.TEXT)
async def add_reminder_step_2(message: types.Message, state: FSMContext):
    if check_coin_id(message.text) != True:
        await message.reply("Choose from the list")
        return
    await state.update_data(coin_id=message.text)
    await ReminderInfo.next()
    await message.answer("Choose time.", reply_markup=kb.time_markup())


@dp.callback_query_handler(lambda c: c.data == "1hour" or c.data == "3hour" or c.data == "6hour" or c.data == "12hour" or c.data == "24hour" ,state=ReminderInfo.waiting_for_reminder_periodisity)
async def add_reminder_step_5(callback_query: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    add_reminder(int(callback_query.from_user.id),get_new_id(callback_query.from_user.id),'simple_typ', True, user_data['coin_id'][1:], callback_query.data[:-4], '2016-06-22 19:10:25', 1.1, )
    await bot.send_message(callback_query.from_user.id, f"We will inform you about the current pirce {user_data['coin_id']}.\n"
                         f"every {callback_query.data}\n")
    await state.finish()

class ReminderDbInfo(StatesGroup):
    waiting_for_reminder_coin_id = State()
    waiting_for_reminder_price_value = State()


@dp.callback_query_handler(lambda c: c.data == "add_reminder_with_bd", state = "*")
async def add_reminderdb_callback(callback_query: types.CallbackQuery):
    await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
    chat_id = callback_query.from_user.id
    coin_list = get_coin_list_for_send()
    await bot.send_message(chat_id, "Choose coin." + coin_list)
    await ReminderDbInfo.waiting_for_reminder_coin_id.set()

@dp.message_handler(state=ReminderDbInfo.waiting_for_reminder_coin_id, content_types=types.ContentTypes.TEXT)
async def add_reminderdb_step_5(message: types.Message, state: FSMContext):
    if check_coin_id(message.text) != True:
        await message.reply("Choose from the list")
        return
    await state.update_data(coin_id=message.text)
    await ReminderDbInfo.next()
    await message.answer("Send your USD value at change on which we will inform you. \n (e.g. every 100USD, if price of BTC change from 45000 to 45100 we inform you) \n Use '.' as a separator if you need ( e.g. 0.5) ")

@dp.message_handler(state=ReminderDbInfo.waiting_for_reminder_price_value, content_types=types.ContentTypes.TEXT)
async def add_reminderdb_step_6(message: types.Message, state: FSMContext):
    check = check_price_value(message.text)
    if check_price_value(message.text) != True:
        await message.reply("Choose from the list")
        return
    user_data = await state.get_data()
    add_reminder(int(message.from_user.id),#TELEGRAM_ID
                get_new_id(message.from_user.id),#REM_ID,
                'value_typ',#REM_TYP
                True,#REM_STATUS
                user_data['coin_id'][1:],#COIN_ID
                float(message.text),#REM_VALUE
                time_now(),#VALUE_TIME
                get_price(user_data['coin_id'][1:]))#LAST_VALUE
                
    await message.answer(f"We will inform you about the current pirce {user_data['coin_id']}.\n"
                     f"every: {message.text} USD")
    await state.finish()