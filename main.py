import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, F
from aiogram.types import ContentType
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.dispatcher import middlewares
from dotenv import load_dotenv
from utils.commands import set_commands
from handlers.start import get_start
from handlers.register import start_register, register_name, register_gender, register_age, register_geo
from handlers.update_location import check_friend
from handlers.say_hello import callback_say_hello
from handlers.profile import places_all
from handlers.create_chat import start_chat_friends, relay_message
from handlers.chats import show_chat, show_first_chat, next_chat, prev_chat, continue_chat, delete_chat
from state.register import RegisterState
from state.chat import ChatStates

from aiogram.filters import Command
from fiters.CheckAdmin import CheckAdmin

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
load_dotenv()

bot = Bot(token=os.getenv("BOT_TOKEN"), parse_mode="HTML")
admin_id = os.getenv("ADMIN_ID")
dp = Dispatcher(storage=MemoryStorage())  # все данные бота будут сохранятся в бд


async def start_bot():
    await bot.send_message(1320680053, text="Бот запущен")

dp.startup.register(start_bot)
dp.message.register(get_start, Command(commands='start'))

#Регистрируем хэнжлер регистрации
dp.message.register(start_register, F.text=='Зарегистрироваться')
dp.message.register(register_name, RegisterState.regName)
dp.message.register(register_age, RegisterState.regAge)
dp.callback_query.register(register_gender, RegisterState.regGender)
dp.message.register(register_geo, RegisterState.regGeo)

#Регистрируем хендлер для запроса на акутальную геолокацию
dp.message.register(check_friend, F.content_type.in_({ContentType.LOCATION}))

#Регистрируем хэндлер для поиска друзей(обновляем геопозицию пользователя)
dp.callback_query.register(places_all, F.data.startswith('find_friends'))

#Отправляем  пользователю приветственное сообщение
dp.callback_query.register(callback_say_hello, lambda c: c.data.startswith('say_hello_'))

#Создать чат между двух пользователей
dp.callback_query.register(start_chat_friends, F.data.startswith('start_chat'))
dp.message.register(relay_message, F.content_type == ContentType.TEXT)

#Обработчик команды chats для показа активных чатов
dp.callback_query.register(show_first_chat, F.data.startswith('chats'))
dp.message.register(show_chat, ChatStates.active_chat)
dp.callback_query.register(next_chat, F.data.startswith('next_chat'))
dp.callback_query.register(prev_chat, F.data.startswith('prev_chat'))
dp.callback_query.register(continue_chat , F.data.startswith('continue_'))
dp.callback_query.register(delete_chat , F.data.startswith('delete_'))




#Завершить чат между пользователями


async def start():
    await set_commands(bot)
    try:
        await dp.start_polling(bot, skip_updates=True)  #запускаем бота в случае не удачи завершаем работу
    finally:
        bot.session.close()

if __name__ == "__main__":
    asyncio.run(start())