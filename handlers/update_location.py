from aiogram import Bot
from aiogram.types import Message
from kb.send_location import update_location
from utils.database import Database
from aiogram.fsm.context import FSMContext
import os


async def check_friend(msg:Message, bot: Bot):
    db = Database(os.getenv('DATABASE_NAME'))
    users = db.select_users_id(msg.from_user.id)
    await msg.answer( f"Привет {users[1]}! \n "
                                       f"Пожалуйста, отправь свою актуальную геолокацию, нажав на кнопку ниже:", reply_markup= update_location)
    await update_location(msg, db)



async def update_location(msg: Message, db: Database):
    latitude = msg.location.latitude
    longitude = msg.location.longitude

    # Обновляем данные геопозиции в базе данных
    user_id = msg.from_user.id
    new_geo = f"{latitude},{longitude}"
    db.update_user_geo(user_id, new_geo)

    await msg.answer("Ваше местоположение успешно обновлено!")