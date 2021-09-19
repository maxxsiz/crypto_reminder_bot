from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 
from misc import dp, bot
from valid_func import check_coin_id, check_time, check_price_value
from db_func import add_reminder, get_new_id
from api import time_now, get_price, get_coin_list

class ReminderInfo(StatesGroup):
    waiting_for_reminder_coin_id = State()
    waiting_for_reminder_periodisity = State()

 
@dp.callback_query_handler(lambda c: c.data == "add_reminder_simple", state = "*")
async def add_reminder_callback(callback_query: types.CallbackQuery):
    chat_id = callback_query.from_user.id
    await bot.delete_message(chat_id, callback_query.message.message_id)
    coin_list = get_coin_list()
    await bot.send_message(chat_id, "Choose coin." + '\n/'.join(' | '.join(("/"+str(key),val)) for (key,val) in coin_list.items()))
    await ReminderInfo.waiting_for_reminder_coin_id.set()

@dp.message_handler(state=ReminderInfo.waiting_for_reminder_coin_id, content_types=types.ContentTypes.TEXT)
async def add_reminder_step_2(message: types.Message, state: FSMContext):
    if check_coin_id(message.text) == False:
        await message.reply("Choose from the list")
        return
    await state.update_data(coin_id=message.text)
    await ReminderInfo.next()
    await message.answer("Choose time.")


@dp.message_handler(state=ReminderInfo.waiting_for_reminder_periodisity, content_types=types.ContentTypes.TEXT)
async def add_reminder_step_5(message: types.Message, state: FSMContext):
    if check_time(message.text) == False:
        await message.reply("Unvalid form. Try again.")
        return
    user_data = await state.get_data()
    await add_reminder(int(message.from_user.id),await get_new_id(),'simple_type', True, user_data['coin_id'], message.text, "-", "-" )
    await message.answer(f"We will inform you about the current pirce {user_data['coin_id']}.\n"
                         f"every {message.text}\n")
    await state.finish()

class ReminderDbInfo(StatesGroup):
    waiting_for_reminder_coin_id = State()
    waiting_for_reminder_price_value = State()


@dp.callback_query_handler(lambda c: c.data == "add_reminder_with_bd", state = "*")
async def add_reminderdb_callback(callback_query: types.CallbackQuery):
    await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
    chat_id = callback_query.from_user.id
    coin_list = get_coin_list()
    await bot.send_message(chat_id, "Choose coin." + '\n/'.join(' | '.join(("/"+str(key),val)) for (key,val) in coin_list.items()))
    await ReminderDbInfo.waiting_for_reminder_coin_id.set()

@dp.message_handler(state=ReminderDbInfo.waiting_for_reminder_coin_id, content_types=types.ContentTypes.TEXT)
async def add_reminderdb_step_5(message: types.Message, state: FSMContext):
    if check_coin_id(message.text) == False:
        await message.reply("Choose from the list")
        return
    await state.update_data(coin_id=message.text)
    await ReminderDbInfo.next()
    await message.answer("Choose your USD value at change on which we will inform you. \n (e.g. every 100USD, if price of BTC change from 45000 to 45100 we inform you)")

@dp.message_handler(state=ReminderDbInfo.waiting_for_reminder_price_value, content_types=types.ContentTypes.TEXT)
async def add_reminderdb_step_6(message: types.Message, state: FSMContext):
    if check_price_value(message.text) == False:
        await message.reply("Unvalid form. Try again.")
        return
    user_data = await state.get_data()
    await add_reminder(int(message.from_user.id),await get_new_id(),'simple_type', True, user_data['coin_id'], message.text, time_now(), get_price[user_data['coin_id']] )
    await message.answer(f"We will inform you about the current pirce {user_data['coin_id']}.\n"
                     f"every: {message.text} USD/USDT")
    await state.finish()