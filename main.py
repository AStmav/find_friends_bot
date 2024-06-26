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
from handlers.register import start_register, register_name, register_phone, register_geo
from handlers.update_location import check_friend
from handlers.say_hello import callback_say_hello
from handlers.profile import places_all
from handlers.create_chat import start_chat_friends, relay_message
from handlers.delete_chat import end_chat
from state.register import RegisterState
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

#Регистрируем хендлер для запроса на акутальную геолокацию

dp.message.register(check_friend, F.content_type.in_({ContentType.LOCATION}))

#Регистрируем хэнжлер регистрации
dp.message.register(start_register, F.text=='Зарегестрироваться')
dp.message.register(register_name, RegisterState.regName)
dp.message.register(register_phone, RegisterState.regPhone)
dp.message.register(register_geo, RegisterState.regGeo)

#Регистрируем хэндлер для поиска друзей(обновляем геопозицию пользователя)
dp.callback_query.register(places_all, F.data.startswith('find_friends'))

#Отправляем  пользователю приветственное сообщение
dp.callback_query.register(callback_say_hello, lambda c: c.data.startswith('say_hello_'))

#Создать чат между двух пользователей
dp.callback_query.register(start_chat_friends, F.data.startswith('start_chat'))
dp.message.register(relay_message, F.content_type == ContentType.TEXT)

#Завершить чат между пользователями
dp.callback_query.register(end_chat, F.data.startswith('end_chat'))


async def start():
    await set_commands(bot)
    try:
        await dp.start_polling(bot, skip_updates=True)#запускаем бота в случае не удачи завершаем работу
    finally:
        bot.session.close()

if __name__ == "__main__":
    asyncio.run(start())