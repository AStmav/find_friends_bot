from utils.database import Database
from aiogram.types import Message, CallbackQuery
from aiogram import Bot
import logging
import os


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def end_chat(call: CallbackQuery, bot: Bot):
    try:
        db = Database(os.getenv('DATABASE_NAME'))
        chat_users = db.get_chat_users(call.from_user.id)

        if chat_users:
            your_id, user_id = chat_users
            if call.from_user.id == your_id:
                other_user_id = user_id
            else:
                other_user_id = your_id

            # Завершаем чат
            db.end_chat(call.from_user.id)

            # Отправляем сообщение о завершении чата
            await bot.send_message(call.from_user.id, "Чат завершен.")
            await bot.send_message(other_user_id, "Чат завершен.")

            # Логируем завершение чата
            logger.info(f"Чат между {your_id} и {user_id} завершен")

            await call.answer("Чат успешно завершен!", show_alert=True)
        else:
            await call.answer("Не удалось найти пользователей для завершения чата.", show_alert=True)
    except Exception as e:
        logger.error(f"Произошла ошибка при завершении чата: {e}")
        await call.answer("Произошла ошибка при завершении чата.", show_alert=True)