from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import Bot
from utils.database import Database
from aiogram.fsm.context import FSMContext
from utils.database import Database
import logging
import os


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def start_chat_friends(call: CallbackQuery, bot: Bot):
    try:
        db = Database(os.getenv('DATABASE_NAME'))
        chat_users = db.get_chat_users(call.from_user.id)

        if chat_users:
            your_id, user_id = chat_users
            if call.from_user.id == your_id:
                other_user_id = user_id
            else:
                other_user_id = your_id

            # Отправляем сообщение о создании чата
            await bot.send_message(call.from_user.id, "Чат успешно создан!")
            await bot.send_message(other_user_id, "Чат успешно создан!")

            # Логируем создание чата
            logger.info(f"Чат между {your_id} и {user_id} создан")

            await call.answer("Чат успешно создан!", show_alert=True)
        else:
            await call.answer("Не удалось найти пользователей для чата.", show_alert=True)
    except Exception as e:
        logger.error(f"Произошла ошибка при начале чата: {e}")
        await call.answer("Произошла ошибка при начале чата.", show_alert=True)


async def relay_message(msg: Message, bot: Bot):
    try:
        db = Database(os.getenv('DATABASE_NAME'))
        chat_users = db.get_chat_users(msg.from_user.id)

        if chat_users:
            your_id, user_id = chat_users
            if msg.from_user.id == your_id:
                other_user_id = user_id
            else:
                other_user_id = your_id

            chat_id = db.get_chat_id(your_id, user_id)
            sender_id = msg.from_user.id
            db.save_message(chat_id, sender_id, msg.text)

            await bot.send_message(other_user_id, msg.text)
            logger.info(f"{msg.from_user.id} to {other_user_id}: {msg.text}")
        else:
            await msg.reply("Чат не активен. Попробуйте начать чат заново.")
    except Exception as e:
        logger.error(f"Произошла ошибка при пересылке сообщения: {e}")
        await msg.reply("Произошла ошибка при отправке сообщения.")


