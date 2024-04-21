from aiogram import F, Router, types
from aiogram.types import Message
from aiogram.filters import Command

import kb
import text

router =Router()

@router.message(Command("start"))
async def start_handler(msg: Message):
    greet_message = text.greet
    await msg.answer(greet_message.format(name=msg.from_user.id), reply_markup=kb.menu)


@router.message(F.text=="Меню")

@router.message(F.text=="Выйти в меню")

@router.message(F.text=="◀️ Выйти в меню")


async def message_handler(msg: Message):
    await msg.answer(text.menu, reply_markup=kb.menu)

