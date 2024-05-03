from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardMarkup, InlineKeyboardButton


find_friends_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Найти друзей', callback_data='find_friends')]
])
