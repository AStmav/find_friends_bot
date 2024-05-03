from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

location_kb = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text='Отправить свое местоположение', request_location=True)

    ]
], request_location=True, resize_keyboard=True, one_time_keyboard=True, input_field_placeholder="Для продолжения нажмите на кнопку ниже")

update_location_kb = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text='Обновить местоположение', request_location=True)
    ]
], resize_keyboard=True, one_time_keyboard=True, input_field_placeholder="Для поиска друзей нажми на кнопку")