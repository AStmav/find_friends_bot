from aiogram import Bot
from aiogram.types import Message
from kb.register import register_kb
from utils.database import Database
from kb.profile import profile_kb
import os

async def get_start(msg:Message, bot: Bot):
    db = Database(os.getenv('DATABASE_NAME'))  # проверяем зарегестрирован ли пользователь ранее
    users = db.select_users_id(msg.from_user.id)
    if (users):
        await bot.send_message(msg.from_user.id, f"Привет {users[1]}!", reply_markup=profile_kb)

    else:
        await bot.send_message(msg.from_user.id, f"Привет! У нас много интересных возможностей для поиска друзей!\n "
                                             f"Для регистрации просто ответьте на это сообщение, и мы проведем вас через процесс регистрации.\n "
                                             f"Буду ждать вашего ответа!", reply_markup=register_kb)