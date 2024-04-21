from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, \
    ReplyKeyboardRemove

menu_buttons = [[InlineKeyboardButton(text="Создать анкету📌", callback_data="registration"),
    InlineKeyboardButton(text="Редактировать анкету📝", callback_data="edit_profile")],
    [InlineKeyboardButton(text="Удалить🗑", callback_data="delete_profile"),
    InlineKeyboardButton(text="Найти человечка🔍", callback_data="find_profile")]]

menu = InlineKeyboardMarkup(inline_keyboard=menu_buttons)
exit_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="◀️ Выйти в меню")]], resize_keyboard=True)
iexit_kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="◀️ Выйти в меню", callback_data="menu")]])
