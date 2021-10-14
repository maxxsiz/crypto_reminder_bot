from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton


def menu_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.one_time_keyboard=True
    markup.add(InlineKeyboardButton("Add reminder", callback_data="add_reminder"),
                InlineKeyboardButton("Control your reminders", callback_data="controll_reminder"),
                InlineKeyboardButton("Show all coin", callback_data="show_stat"),
                InlineKeyboardButton("Show all reminders", callback_data="other"),
                InlineKeyboardButton("Cancel", callback_data="cancel"))
    return markup

def controll_reminder_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.one_time_keyboard=True
    markup.add(InlineKeyboardButton("Delete reminder", callback_data="delete_reminder"),
                InlineKeyboardButton("Freeze/unfreeze reminder", callback_data="freeze_reminder"),
                InlineKeyboardButton("Edit reminder", callback_data="edit_reminder"),
                InlineKeyboardButton("Cancel", callback_data="cancel"))

    return markup

def add_reminder_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.one_time_keyboard=True
    markup.add(InlineKeyboardButton("Add reminder with timer.", callback_data="add_reminder_simple"),
                InlineKeyboardButton("Add reminder with value.", callback_data="add_reminder_with_bd"),
                InlineKeyboardButton("Cancel", callback_data="cancel"))
    return markup

def yes_no_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.one_time_keyboard=True
    markup.add(InlineKeyboardButton("Yes", callback_data="answer_yes"),
                InlineKeyboardButton("No", callback_data="answer_no"))
    return markup


def time_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.one_time_keyboard=True
    markup.add(InlineKeyboardButton("every 1 hour", callback_data="1hour"),
                InlineKeyboardButton("every 3 hour", callback_data="3hour"),
                InlineKeyboardButton("every 6 hour", callback_data="6hour"),
                InlineKeyboardButton("at 09:00 and 21:00", callback_data="12hour"),
                InlineKeyboardButton("every day at 09:00", callback_data="24hour"))
    return markup