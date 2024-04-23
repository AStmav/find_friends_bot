from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

register_kb = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(
            text='Зарегестрироваться'
        )
    ]
], resize_keyboard=True, one_time_keyboard=True, input_field_placeholder="Для продолжения нажмите на кнопку ниже")

