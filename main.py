import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, F
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv
from utils.commands import set_commands
from handlers.start import get_start
from handlers.register import start_register, register_name, register_phone
from state.register import RegisterState
from aiogram.filters import Command

load_dotenv()

bot = Bot(token=os.getenv("BOT_TOKEN"), parse_mode="HTML")
admin_id = os.getenv("ADMIN_ID")
dp = Dispatcher(storage=MemoryStorage())  # все данные бота будут сохранятся в бд



async def start_bot():
    await bot.send_message(admin_id, text="Бот запущен")

dp.startup.register(start_bot)
dp.message.register(get_start, Command(commands='start'))

#Регистрируем хэнжлер регистрации
dp.message.register(start_register, F.text=="Зарегестрироваться")
dp.message.register(register_name, RegisterState.regName)
dp.message.register(register_phone, RegisterState.regPhone)
async def start():
    await set_commands(bot)
    try:
        await dp.start_polling(bot, skip_updates=True)#запускаем бота в случае не удачи завершаем работу
    finally:
        bot.session.close()

if __name__ == "__main__":
    asyncio.run(start())