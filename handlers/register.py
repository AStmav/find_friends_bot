from aiogram import Bot
from aiogram.types import Message,location
from aiogram.fsm.context import FSMContext
from state.register import RegisterState
from kb.send_location import location_kb
import re
import os
from utils.database import Database




async def start_register(msg:Message, state:FSMContext, bot:Bot):
    db = Database(os.getenv('DATABASE_NAME')) #проверяем зарегестрирован ли пользователь ранее
    users = db.select_users_id(msg.from_user.id)
    if (users):
        await bot.send_message(msg.from_user.id, f"{users[1]} \n  Вы уже зарегестрированы")
    else:
        await bot.send_message(msg.from_user.id,f"Давайте зарегестрируемся 📌\n Для начала введи Ваше имя📝")
        await state.set_state(RegisterState.regName)

async def register_name(msg:Message, state:FSMContext, bot:Bot):
    await bot.send_message(msg.from_user.id,f"Приятно познакомиться {msg.text} \n"
                     f"Теперь укажите номер телефона, чтобы быть на связи \n"
                     f"☎️ Формат телефона: +7xxxxxxxxxx\n\n"
                     f"⚠️ Внимание! Я чувствителен к формату ввода номера телефона ⚠️")
    await state.update_data(register_name=msg.text)
    await state.set_state(RegisterState.regPhone)

async def register_phone(msg:Message, state:FSMContext, bot:Bot):
    if (re.findall('^\+?[7][-\(]?\d{3}\)?-?\d{3}-?\d{2}-?\d{2}$', msg.text)):
        await state.update_data(register_phone=msg.text)
        msg_success = (f"Ваш номер телефон:{msg.text} \n"
                       f"Теперь укажите Вашу геолокацию 🌍 чтобы я помог Вам найти друзей рядом с Вами")
        await bot.send_message(msg.from_user.id,msg_success)
        await state.update_data(register_phone=msg.text)
        await state.set_state(RegisterState.regGeo)

    else:
        await bot.send_message(msg.from_user.id,f"Номер указан в неправильном формате ")


async def register_geo(msg:Message, state:FSMContext, bot:Bot):
    latitude = msg.location.latitude
    longitude = msg.location.longitude
    await bot.send_location(msg.chat.id, latitude, longitude)
    await bot.send_message(msg.from_user.id, f"Широта: {latitude}, Долгота: {longitude}")
    await state.update_data(latitude=latitude, longitude=longitude)

    reg_data = await state.get_data()
    reg_name = reg_data.get('register_name')
    reg_phone = reg_data.get('register_phone')
    reg_geo = f"{latitude},{longitude}"

    msg_success = f"Приятно познакомиться {reg_name} \n\n  Телефон:{reg_phone} Геопозиция: {reg_geo}"
    await bot.send_message(msg.from_user.id,msg_success)

    db = Database(os.getenv('DATABASE_NAME'))
    db.add_user(reg_name,reg_phone,reg_geo, msg.from_user.id)

    await state.clear()




