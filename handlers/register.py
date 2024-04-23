from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from state.register import RegisterState
import re
import os
from utils.database import Database




async def start_register(msg:Message, state:FSMContext):
    db = Database(os.getenv('DATABASE_NAME')) #проверяем зарегестрирован ли пользователь ранее
    users = db.select_users_id(msg.from_user.id)
    if (users):
        await msg.answer(f"{users[1]} \n  Вы уже зарегестрированы")
    else:
        await msg.answer(f"Давайте зарегестрируемся 📌\n Для начала введи Ваше имя📝")
        await state.set_state(RegisterState.regName)

async def register_name(msg:Message, state:FSMContext):
    await msg.answer(f"Приятно познакомиться {msg.text} \n"
                     f"Теперь укажите номер телефона, чтобы быть на связи \n"
                     f"☎️ Формат телефона: +7xxxxxxxxxx\n\n"
                     f"⚠️ Внимание! Я чувствителен к формату ввода номера телефона ⚠️")
    await state.update_data(register_name=msg.text)
    await state.set_state(RegisterState.regPhone)

async def register_phone(msg:Message, state:FSMContext):
    if (re.findall('^\+?[7][-\(]?\d{3}\)?-?\d{3}-?\d{2}-?\d{2}$', msg.text)):
        await state.update_data(register_phone=msg.text)
        reg_data = await state.get_data()
        reg_name = reg_data.get('register_name')
        reg_phone = reg_data.get('register_phone')
        msg_success = f"Приятно познакомиться {reg_name} \n\n  Телефон:{reg_phone}"
        await msg.answer(msg_success)
        db = Database(os.getenv('DATABASE_NAME'))
        db.add_user(reg_name,reg_phone,msg.from_user.id)

        await state.clear()

    else:
        await msg.answer(f"Номер указан в неправильном формате")


