from aiogram.utils.keyboard import InlineKeyboardMarkup, InlineKeyboardButton

gender_kb = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Мужской", callback_data="gender_male"),
        InlineKeyboardButton(text="Женский", callback_data="gender_female")
    ]
])