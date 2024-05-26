from aiogram import Bot
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import Bot
from utils.database import Database
from aiogram.fsm.context import FSMContext
from utils.database import Database
from handlers.profile import places_all
from handlers.say_hello import callback_say_hello
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

            button_end_chat = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="Завершить беседу", callback_data="end_chat")]
            ])
            await bot.send_message(call.from_user.id, "Чтобы завершить чат, нажмите кнопку ниже.",
                                   reply_markup=button_end_chat)
            await bot.send_message(other_user_id, "Чтобы завершить чат, нажмите кнопку ниже.",
                                   reply_markup=button_end_chat)
            # Логируем создание чата
            logger.info(f"Чат между {your_id} и {user_id} создан")

            await call.answer("Чат успешно создан!", show_alert=True)
        else:
            await call.answer("Не удалось найти пользователей для чата.", show_alert=True)
    except Exception as e:
        logger.error(f"Произошла ошибка при начале чата: {e}")
        await call.answer("Произошла ошибка при начале чата.", show_alert=True)


async def relay_message(msg:Message, bot: Bot):
    try:
        db = Database(os.getenv('DATABASE_NAME'))
        chat_users = db.get_chat_users(msg.from_user.id)

        if chat_users:
            your_id, user_id = chat_users
            if msg.from_user.id == your_id:
                other_user_id = user_id
            else:
                other_user_id = your_id

            await bot.send_message(other_user_id, msg.text)
            logger.info(f"{msg.from_user.id} to {other_user_id}: {msg.text}")
        else:
            await msg.reply("Чат не активен. Попробуйте начать чат заново.")
    except Exception as e:
        logger.error(f"Произошла ошибка при пересылке сообщения: {e}")
        await msg.reply("Произошла ошибка при отправке сообщения.")


# user1_id = 1320680053
# user2_id = 1787078931

# async def start_chat_friends(call: CallbackQuery, bot:Bot):
#     global chat_active
#     try:
#         # Активируем чат
#         chat_active = True
#
#         # Отправляем сообщение о создании чата
#         await bot.send_message(user1_id, "Чат успешно создан!")
#         await bot.send_message(user2_id, "Чат успешно создан!")
#
#         # Логируем создание чата
#         logger.info(f"Чат между {user1_id} и {user2_id} создан")
#     except Exception as e:
#         logger.error(f"Произошла ошибка при начале чата: {e}")
#         await call.answer("Произошла ошибка при начале чата.", show_alert=True)
#
# # Функция для пересылки сообщений между пользователями
# async def relay_message(msg: Message, bot:Bot):
#     global chat_active
#     try:
#         if not chat_active:
#             await msg.reply("Чат не активен. Попробуйте начать чат заново.")
#             return
#
#         logger.info(f"Received message from {msg.from_user.id}: {msg.text}")
#
#         if msg.from_user.id == user1_id:
#             await bot.send_message(user2_id, msg.text)
#             logger.info(f"{user1_id} to {user2_id}: {msg.text}")
#         elif msg.from_user.id == user2_id:
#             await bot.send_message(user1_id, msg.text)
#             logger.info(f"{user2_id} to {user1_id}: {msg.text}")
#         else:
#             logger.warning(f"Сообщение от неизвестного пользователя: {msg.from_user.id}")
#     except Exception as e:
#         logger.error(f"Произошла ошибка при пересылке сообщения: {e}")
#         await msg.reply("Произошла ошибка при отправке сообщения.")
