from aiogram import Bot
from aiogram.types import Message, ReplyKeyboardRemove
from kb.find_friends import find_friends_kb
from utils.database import Database
from state.update_location import UpdateState
from aiogram.fsm.context import FSMContext
import os


async def check_friend(msg: Message, state: FSMContext, bot: Bot):
    db = Database(os.getenv('DATABASE_NAME'))
    users = db.select_users_id(msg.from_user.id)
    if msg.location:
        latitude = msg.location.latitude
        longitude = msg.location.longitude
        user_id = msg.from_user.id
        new_geo = f"{latitude},{longitude}"
        db.update_user_geo(user_id, new_geo)
        await msg.answer(f"Ваше местоположение успешно обновлено ✅  {new_geo}", reply_markup=ReplyKeyboardRemove())
        await state.set_state(UpdateState.updateGeo)
        await bot.send_message(msg.from_user.id, "Теперь вы можете найти друзей поблизости:",
                               reply_markup=find_friends_kb)

    else:
        await msg.answer("Вы не отправили своё местоположение.")
        return  # Выходим из функции, если местоположение не было отправлено

    # Отправляем кнопку "Найти друзей"



