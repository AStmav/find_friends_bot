from aiogram import Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from utils.database import Database
from handlers.profile import places_all
from handlers.say_hello import callback_say_hello
from state.create_chat import CreateChatState
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

user1_id = 1320680053
user2_id= 1787078931

async def start_chat_friends(call:CallbackQuery, bot:Bot, state: FSMContext): #Обработка нажатия на кнопку "начать общение"

    try:
        # Устанавливаем состояние чата
        await state.set_state(CreateChatState.CreateChat)
        await state.update_data(user1_id=user1_id, user2_id=user2_id)

        # Отправляем сообщение о создании чата
        await bot.send_message(user1_id, "Чат успешно создан!")
        await bot.send_message(user2_id, "Чат успешно создан!")

        # Логируем создание чата
        logger.info(f"Чат между  {user1_id} and {user2_id}")

    except Exception as e:
        logger.error(f"An error occurred while starting chat: {e}")
        await call.answer("Произошла ошибка при начале чата.", show_alert=True)


async def relay_message(msg: Message, state: FSMContext, bot:Bot):
    try:
        data = await state.get_data()
        user1_id = data.get("user1_id")
        user2_id = data.get("user2_id")

        if msg.from_user.id == user1_id:
            await bot.send_message(user2_id, msg.text)
        elif msg.from_user.id == user2_id:
            await bot.send_message(user1_id, msg.text)
    except Exception as e:
        logger.error(f"An error occurred while relaying message: {e}")
        await msg.reply("Произошла ошибка при отправке сообщения.")