from aiogram import Bot
from aiogram.types import Message
from kb.register import register_kb
from kb.send_location import update_location_kb
from utils.database import Database

import os

async def get_start(msg:Message, bot: Bot):
    db = Database(os.getenv('DATABASE_NAME'))  # проверяем зарегестрирован ли пользователь ранее
    users = db.select_users_id(msg.from_user.id)
    if (users):
        await msg.answer( f"Привет, {users[1]} 👋 \n "
                                       f"Пожалуйста, отправь свою актуальную геолокацию 🌍, нажав на кнопку ниже:", reply_markup=update_location_kb)


    else:
        await bot.send_message(msg.from_user.id, f"👋 Привет! Добро пожаловать в наш бот для знакомств! 🌟\n\n"
        "Здесь вы можете найти новых друзей . \n"
        "Начнем регистрацию, чтобы вы могли быстрее приступить к поиску! 📝\n\n"
        "Нажмите на кнопку - ✅ Зарегистрироваться" , reply_markup=register_kb)