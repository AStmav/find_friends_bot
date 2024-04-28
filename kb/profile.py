from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# profile_kb = ReplyKeyboardMarkup(keyboard=[
#     [
#         KeyboardButton(
#             text='Найти друзей'
#         )
#     ]
# ], resize_keyboard=True, one_time_keyboard=True, input_field_placeholder="Для поиска друзей нажми на кнопку")

profile_kb = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text='Найти друзей'),
        KeyboardButton(text='Обновить местоположение', request_location=True)
    ]
], resize_keyboard=True, one_time_keyboard=True, input_field_placeholder="Для поиска друзей нажми на кнопку")