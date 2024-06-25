from aiogram import Bot
from aiogram.types import Message,CallbackQuery
from aiogram.fsm.context import FSMContext
from state.register import RegisterState
import re
import os
from utils.database import Database
from kb.send_location import location_kb
from kb.your_gender import gender_kb
from kb.find_friends import find_friends_kb




async def start_register(msg:Message, state:FSMContext, bot:Bot):
    db = Database(os.getenv('DATABASE_NAME')) #проверяем зарегестрирован ли пользователь ранее
    users = db.select_users_id(msg.from_user.id)
    if (users):
        await bot.send_message(msg.from_user.id, f"{users[1]} \nВы уже зарегестрированы")
    else:
        await bot.send_message(msg.from_user.id,f"Отлично 👍 \nДавайте знакомиться, напишите Ваше имя 📝")
        await state.set_state(RegisterState.regName)

async def register_name(msg:Message, state:FSMContext, bot:Bot):
    await bot.send_message(msg.from_user.id,f"Приятно познакомиться, {msg.text} \n"
                     f"Теперь укажите Ваш возраст \n"
                     f"⚠️Если Вам уже исполнилось 18 лет⚠️\n\n")
    await state.update_data(register_name=msg.text)
    await state.set_state(RegisterState.regAge)

async def register_age(msg: Message, state: FSMContext, bot: Bot):
    try:
        age = int(msg.text)
        if age >= 18:
            await state.update_data(register_age=age)
            msg_success = (f"Ваш возраст: {age} \n"
                           f"Теперь укажите Ваш пол 👌")
            await bot.send_message(msg.from_user.id, msg_success, reply_markup=gender_kb)
            await state.set_state(RegisterState.regGender)
        else:
            await bot.send_message(msg.from_user.id, "Регистрация доступна только для пользователей старше 18 лет.")
            await state.clear()
    except ValueError:
        await bot.send_message(msg.from_user.id, "Пожалуйста, введите корректный возраст.")

async def register_gender(call: CallbackQuery, state: FSMContext, bot: Bot):
    gender = None
    if call.data == "gender_male":
        gender = "Мужской"
    elif call.data == "gender_female":
        gender = "Женский"

    if gender:
        await state.update_data(register_gender=gender)
        msg_success = (f"Ваш пол: {gender} \n\n"
                       f"Нажмите на кнопку: 🌍Отправить свое местоположение🌍 \n чтобы я помог вам найти друзей рядом с вами")
        await bot.send_message(call.from_user.id, msg_success, reply_markup=location_kb)
        await state.set_state(RegisterState.regGeo)
    else:
        await bot.send_message(call.from_user.id, "Пожалуйста, выберите пол, используя кнопки на клавиатуре.")


async def register_geo(msg:Message, state:FSMContext, bot:Bot):
    latitude = msg.location.latitude
    longitude = msg.location.longitude
    await bot.send_location(msg.chat.id, latitude, longitude)
    await bot.send_message(msg.from_user.id, f"Широта: {latitude}, Долгота: {longitude}")
    await state.update_data(latitude=latitude, longitude=longitude)

    reg_data = await state.get_data()
    reg_name = reg_data.get('register_name')
    reg_age = reg_data.get('register_age')
    reg_gender = reg_data.get('register_gender')
    reg_geo = f"{latitude},{longitude}"

    msg_success = f"Приятно познакомиться : {reg_name} \n\n  Возраст :{reg_age} \n\n Пол :{reg_gender} \n\n Геопозиция : {reg_geo} "
    await bot.send_message(msg.from_user.id,msg_success)

    db = Database(os.getenv('DATABASE_NAME'))
    db.add_user(reg_name, reg_age, reg_gender, reg_geo,  msg.from_user.id)
    await bot.send_message(msg.from_user.id, "Регистрация завершена 👍 Теперь вы можете найти друзей поблизости. ✅",
                           reply_markup=find_friends_kb)

    await state.clear()




