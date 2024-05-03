from aiogram import Bot
from aiogram.types import Message
from kb.register import register_kb
#from handlers.update_location import check_friend
from kb.send_location import update_location_kb
from utils.database import Database

import os

async def get_start(msg:Message, bot: Bot):
    db = Database(os.getenv('DATABASE_NAME'))  # проверяем зарегестрирован ли пользователь ранее
    users = db.select_users_id(msg.from_user.id)
    if (users):
        await msg.answer( f"Привет {users[1]}! \n "
                                       f"Пожалуйста, отправь свою актуальную геолокацию, нажав на кнопку ниже:", reply_markup=update_location_kb)


    else:
        await bot.send_message(msg.from_user.id, f"Привет! У нас много интересных возможностей для поиска друзей!\n "
                                             f"Для регистрации просто ответьте на это сообщение (НАЖМИТЕ НА КНОПКУ ЗАРЕГЕСТРИРОВАТЬСЯ), и мы проведем вас через процесс регистрации.\n "
                                             f"Буду ждать вашего ответа!", reply_markup=register_kb)