from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton


def menu_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.one_time_keyboard=True
    markup.add(InlineKeyboardButton("Add reminder", callback_data="add_reminder"),
                InlineKeyboardButton("Control your reminders", callback_data="controll_reminder"),
                InlineKeyboardButton("Show all data", callback_data="show_stat"),
                InlineKeyboardButton("Other", callback_data="other"))
    return markup

def controll_reminder_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.one_time_keyboard=True
    markup.add(InlineKeyboardButton("Delete reminder", callback_data="delete_reminder"),
                InlineKeyboardButton("Stop reminder", callback_data="freeze_reminder"),
                InlineKeyboardButton("Edit reminder", callback_data="edit_reminder"))
    return markup

def add_reminder_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.one_time_keyboard=True
    markup.add(InlineKeyboardButton("Add constantly reminder.", callback_data="add_reminder_simple"),
                InlineKeyboardButton("Add reminder with value.", callback_data="add_reminder_with_bd"))
    return markup

def edit_reminder_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.one_time_keyboard=True
    markup.add(InlineKeyboardButton("Змінити назву нагадування", callback_data="edit_name"),
                InlineKeyboardButton("Змінити назву нагадування", callback_data="edit_description"),
                InlineKeyboardButton("Змінити частоту нагадування", callback_data="edit_periodicity"),
                InlineKeyboardButton("Змінити період перериву", callback_data="edit_break_time"))
    return markup



def yes_no_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.one_time_keyboard=True
    markup.add(InlineKeyboardButton("Yes", callback_data="answer_yes"),
                InlineKeyboardButton("No", callback_data="answer_no"))
    return markup