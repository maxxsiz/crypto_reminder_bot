from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 
from misc import dp, bot
import keyboards as kb
from valid_func import check_price_value, check_reminder_id
from db_func import delete_reminder, freeze_reminder, edit_reminder, check_status, show_all_reminders

class ReminderDelete(StatesGroup):
    waiting_for_reminder_id = State()
    waiting_for_check = State()

@dp.callback_query_handler(lambda c: c.data == "delete_reminder", state = "*")
async def delete_reminder_step_1(callback_query: types.CallbackQuery):
    chat_id = callback_query.from_user.id
    await bot.delete_message(chat_id, callback_query.message.message_id)
    await bot.send_message(chat_id, "Choose reminder for DELETE")
    await bot.send_message(chat_id, await show_all_reminders(chat_id))
    await ReminderDelete.waiting_for_reminder_id.set()

@dp.message_handler(state=ReminderDelete.waiting_for_reminder_id, content_types=types.ContentTypes.TEXT)
async def delete_reminder_step_2(message: types.Message, state: FSMContext):
    if int(message.text[1:]) in "all reminders list" :
        await message.reply("Choose the number from list")
        return
    await state.update_data(reminder_id=message.text[1:])
    await ReminderDelete.next()
    await message.answer(f"Do you really want to delete the reminder {message.text}",reply_markup=kb.yes_no_markup())

@dp.callback_query_handler(lambda c: c.data == "answer_yes" or c.data == "answer_no" , state=ReminderDelete.waiting_for_check)
async def delete_reminder_step_3(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
    user_data = await state.get_data()
    if callback_query.data == "answer_yes":
        await delete_reminder(user_data['reminder_id'])
        await bot.send_message(callback_query.from_user.id, f"Remider {user_data['reminder_id']} successfully deleted.")
    elif callback_query.data == "answer_no":
        await bot.send_message(callback_query.from_user.id, "Deleting was canceled")
    await state.finish()

#freeze reminder

class ReminderFreeze(StatesGroup):
    waiting_for_reminder_id = State()
    waiting_for_check = State()

@dp.callback_query_handler(lambda c: c.data == "freeze_reminder", state = "*")
async def freeze_reminder_step_1(callback_query: types.CallbackQuery):
    chat_id = callback_query.from_user.id
    await bot.delete_message(chat_id, callback_query.message.message_id)
    await bot.send_message(chat_id, "Choose reminder for freeze/unfreeze")
    await bot.send_message(chat_id, await show_all_reminders(chat_id))
    await ReminderFreeze.waiting_for_reminder_id.set()

@dp.message_handler(state=ReminderFreeze.waiting_for_reminder_id, content_types=types.ContentTypes.TEXT)
async def freeze_reminder_step_2(message: types.Message, state: FSMContext):
    if int(message.text[1:]) in "all reminders list":
        await message.reply("Choose the number from list")
        return
    rm_status = check_status()
    new_rm_status = lambda rm_status: False if rm_status == 1 else True
    await state.update_data(reminder_id=message.text[1:], reminder_status = new_rm_status(rm_status))
    if rm_status == 1:
        await message.answer(f"You really want to deactivate reminder {message.text}",reply_markup=kb.yes_no_markup())
    else: 
        await message.answer(f"You really want to activate reminder {message.text}",reply_markup=kb.yes_no_markup())
    await ReminderFreeze.next()

@dp.callback_query_handler(lambda c: c.data == "answer_yes" or c.data == "answer_no" , state=ReminderFreeze.waiting_for_check)
async def freeze_reminder_step_3(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
    if callback_query.data == "answer_yes":
        user_data = await state.get_data()
        await freeze_reminder(user_data['reminder_id'])
        await bot.send_message(callback_query.from_user.id, f"Reminder {user_data['reminder_id']} successfully freeze.")
    elif callback_query.data == "answer_no":
        await bot.send_message(callback_query.from_user.id, "Freezing was canceled.")
    await state.finish()


class ReminderEdit(StatesGroup):
    waiting_for_reminder_id = State()
    waiting_for_new_value_time = State()
    waiting_for_check = State()


@dp.callback_query_handler(lambda c: c.data == "edit_reminder", state = "*") # first step send reminders_list
async def edit_reminder_step_1(callback_query: types.CallbackQuery):
    chat_id = callback_query.from_user.id
    await bot.delete_message(chat_id, callback_query.message.message_id)
    await bot.send_message(chat_id, "Choose reminder for edit")
    await bot.send_message(chat_id, await show_all_reminders(chat_id))
    await ReminderEdit.waiting_for_reminder_id.set()

@dp.message_handler(state=ReminderEdit.waiting_for_reminder_id, content_types=types.ContentTypes.TEXT) # choose reminder, and send edit inlinebutton
async def edit_reminder_name(message: types.Message, state: FSMContext):
    if check_reminder_id(message.text.lower()) == False:
        await message.reply("Choose the number from list")
        return
    await state.update_data(reminder_id=message.text)
    await ReminderEdit.next()
    await message.answer("Choose time / value.")

@dp.message_handler(state=ReminderEdit.waiting_for_new_value_time, content_types=types.ContentTypes.TEXT) # choose reminder, and send edit inlinebutton
async def edit_reminder_name(message: types.Message, state: FSMContext):
    if check_price_value(message.text.lower()) == False:
        await message.reply("Unvalid form. Try again.")
        return
    await state.update_data(new_value=message.text)
    await ReminderEdit.next()
    await message.answer("Choose time / value.")



@dp.callback_query_handler(lambda c: c.data == "answer_yes" or c.data == "answer_no" , state=ReminderEdit.waiting_for_check)
async def freeze_reminder_step_3(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
    if callback_query.data == "answer_yes":
        user_data = await state.get_data()
        #reminder_freeze(user_data['reminder_id'], user_data['reminder_status'])
        await bot.send_message(callback_query.from_user.id, f"Reminder {user_data['reminder_id']} successfully changed, new value/time {user_data['new_value']}.")
    elif callback_query.data == "answer_no":
        await bot.send_message(callback_query.from_user.id, "Changing was canceled.")
    await state.finish()
    

