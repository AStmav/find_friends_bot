import math
import os
from aiogram import Bot
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from utils.database import Database
from math import radians, sin, cos, sqrt, atan2





async def places_all(call: CallbackQuery, state: FSMContext, bot: Bot):
    db = Database(os.getenv('DATABASE_NAME'))

    # Получение местоположения пользователя
    user_geo_str = db.select_place_user(call.from_user.id)
    if not user_geo_str:
        await bot.send_message(call.from_user.id, "Местоположение пользователя не найдено.")
        return

    user_geo_values = user_geo_str[0].split(',')
    user_lat = radians(float(user_geo_values[0]))
    user_lon = radians(float(user_geo_values[1]))

    user_data = db.select_users_id(call.from_user.id)
    if not user_data:
        await bot.send_message(call.from_user.id, "Пользователь не найден.")
        return
    user_gender = user_data[3]

    # Определение противоположного пола
    opposite_gender = "Мужской" if user_gender == "Женский" else "Женский"

    # Получение всех местоположений из базы данных
    all_geo = db.select_places_all()

    R = 6371.0
    friends = []

    # Проверка расстояния между пользователями
    for geo in all_geo:
        geo_values = geo[1].split(',')  # Извлекаем координаты из кортежа
        geo_name = geo[0]  # Имя пользователя
        geo_id_user = geo[2]  # id телеграмм
        geo_gender = geo[3]  # пол пользователя
        geo_age = geo[4]  # возраст пользователя

        # Пропуск своих координат и пользователей одного пола
        if geo[1] == user_geo_str[0] or geo_gender != opposite_gender:
            continue

        lat2 = radians(float(geo_values[0]))
        lon2 = radians(float(geo_values[1]))

        # Разница широт и долгот
        dlon = lon2 - user_lon
        dlat = lat2 - user_lat

        # Вычисление расстояния с помощью формулы Гаверсинуса
        a = sin(dlat / 2) ** 2 + cos(user_lat) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        distance = R * c

        if distance <= 1.0:
            button_text = f'Отправить привет {geo_name}, возраст: {geo_age}'
            button_data = f'say_hello_{geo_id_user}'
            friends.append(InlineKeyboardButton(text=button_text, callback_data=button_data))

    # Отправка сообщения о друзьях рядом
    if friends:
        # Сохраняем ID пользователя, который ищет друзей, в состояние FSMContext
        await state.update_data(seeker_id=call.from_user.id)
        find_friends_kb = InlineKeyboardMarkup(inline_keyboard=[[button] for button in friends])
        await bot.send_message(call.from_user.id, "Выберите друга для отправки привета:",
                               reply_markup=find_friends_kb)
    else:
        await bot.send_message(call.from_user.id, "Друзей рядом нет.")
