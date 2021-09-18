from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.webhook import SendMessage
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import types
from db_func import show_all_reminders
from api import get_coin_list

import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

import keyboards as kb
from misc import dp, bot


@dp.callback_query_handler(lambda c: c.data, state = "*")
async def process_all_callback(callback_query: types.CallbackQuery):
    chat_id = callback_query.from_user.id
    message_id = callback_query.message.message_id
    if callback_query.data == "add_reminder":
        await bot.delete_message(chat_id, message_id)
        await bot.send_message(chat_id,"Виберіть, що Вас цікавить.", reply_markup=kb.add_reminder_markup())
    elif callback_query.data == "controll_reminder":
        await bot.delete_message(chat_id, message_id)
        await bot.send_message(chat_id,"Виберіть, що Вас цікавить.", reply_markup=kb.controll_reminder_markup())
    elif callback_query.data == "show_stat":
        await bot.delete_message(chat_id, message_id)
        await bot.send_message(chat_id, await get_coin_list())
    elif callback_query.data == "show_reminders":
        await bot.delete_message(chat_id, message_id)
        await bot.send_message(chat_id, await show_all_reminders(chat_id))
    elif callback_query.data == "other":
        await bot.delete_message(chat_id, message_id)
        await bot.send_message(chat_id, await show_all_reminders(chat_id))