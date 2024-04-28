import math
import os
from aiogram import Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from utils.database import Database
from math import radians, sin, cos, sqrt, atan2


# async def places_all(msg:Message, state:FSMContext, bot:Bot):
#     db = Database(os.getenv('DATABASE_NAME'))
#     places = db.select_places_all()
#     await bot.send_message(msg.from_user.id, f"Это все друзья рядом:{places}")


async def places_all(msg: Message, state: FSMContext, bot: Bot):
    db = Database(os.getenv('DATABASE_NAME'))

    # Получение местоположения пользователя
    user_geo_str = db.select_place_user(msg.from_user.id)
    if not user_geo_str:
        await bot.send_message(msg.from_user.id, "Местоположение пользователя не найдено.")
        return

    user_geo_values = user_geo_str[0].split(',')
    user_lat = radians(float(user_geo_values[0]))
    user_lon = radians(float(user_geo_values[1]))

    # Получение всех местоположений из базы данных
    all_geo = db.select_places_all()

    R = 6371.0
    friends = []

    # Проверка расстояния между пользователями
    for geo in all_geo:
        geo_values = geo[1].split(',')  # Извлекаем координаты из кортежа
        geo_name = geo[0]  # Имя пользователя
        if geo[1] == user_geo_str[0]:
            continue  # Пропустить свои координаты
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
            friends.append(geo_name)  # Добавляем пользователя в список друзей


    # Отправка сообщения о друзьях рядом
    if friends:
         # Убираем координаты пользователя # Убираем координаты пользователя
        await bot.send_message(msg.from_user.id, f"Друзья рядом : {friends}")
    else:
        await bot.send_message(msg.from_user.id, "Друзей рядом нет.")


