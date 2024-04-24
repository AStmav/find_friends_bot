from aiogram import Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

async def create(msg:Message, state: FSMContext, bot:Bot):
    await bot.send_message(msg.from_user.id, f'Create is load')