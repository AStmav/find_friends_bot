from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardMarkup, InlineKeyboardButton
from utils.database import Database
from aiogram.fsm.context import FSMContext
from state.chat import ChatStates
import os
import logging
from aiogram import Bot




logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def show_first_chat(call:CallbackQuery, state: FSMContext): #первый чат
    db = Database(os.getenv('DATABASE_NAME'))
    user_id = call.from_user.id
    print(user_id)
    active_chats = db.get_active_chats(user_id)
    print(f"Active chats for user {user_id}: {active_chats}")

    if not active_chats:
        await call.answer("У вас нет активных чатов.")
        return

    #await state.update_data(active_chats=active_chats, chat_index=0)
    #await show_chat(call, state)
    await state.update_data(active_chats=active_chats, chat_index=0)
    await state.set_state(ChatStates.active_chat)
    await show_chat(call.message, state)



async def show_chat(msg: Message, state: FSMContext):
    data = await state.get_data()
    print(data)
    active_chats = data['active_chats']
    print(active_chats)
    chat_index = data['chat_index']
    print(chat_index)

    if not active_chats or chat_index < 0 or chat_index >= len(active_chats):
        await msg.answer("Нет доступных чатов.")
        return

    chat = active_chats[chat_index]
    nickname = chat['user_name']
    chat_id = chat['chat_id']

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Общаться", callback_data=f"continue_{chat_id}"),
            InlineKeyboardButton(text="Удалить", callback_data=f"delete_{chat_id}")
        ],
        [
            InlineKeyboardButton(text="Назад", callback_data="prev_chat"),
            InlineKeyboardButton(text="Вперед", callback_data="next_chat")
        ]
    ])

    await msg.answer(f"Чат с: {nickname}", reply_markup=keyboard)

async def next_chat(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    active_chats = data.get('active_chats', [])
    chat_index = data.get('chat_index', 0)

    if not active_chats:
        await callback_query.message.answer("Нет доступных чатов.")
    elif chat_index < len(active_chats) - 1:
        chat_index += 1
        await state.update_data(chat_index=chat_index)
        await show_chat(callback_query.message, state)
    else:
        await callback_query.message.answer("Больше чатов нет.")

    await callback_query.answer()


async def prev_chat(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    active_chats = data['active_chats']
    chat_index = data['chat_index']

    if not active_chats:
        await callback_query.message.answer("Нет доступных чатов.")
    elif chat_index < len(active_chats) - 1:
        chat_index -= 1
        await state.update_data(chat_index=chat_index)
        await show_chat(callback_query.message, state)
    else:
        await callback_query.message.answer("Больше чатов нет.")

    await callback_query.answer()


#dp.callback_query_handler(lambda c: c.data.startswith('continue_'))
async def continue_chat(callback_query: CallbackQuery, bot:Bot):
    chat_id = int(callback_query.data.split('_')[1])
    user_id = callback_query.from_user.id

    # Инициализация базы данных
    db = Database(os.getenv('DATABASE_NAME'))

    # Извлечь переписку из базы данных
    messages = await db.get_chat_messages(chat_id)

    # Отправить переписку пользователю
    for msg in messages:
        await bot.send_message(user_id, msg['text'])

    await callback_query.answer("Продолжаем общение.")


async def delete_chat(callback_query: CallbackQuery, state: FSMContext, bot: Bot):
    chat_id = int(callback_query.data.split('_')[1])
    user_id = callback_query.from_user.id

    # Инициализация базы данных
    db = Database(os.getenv('DATABASE_NAME'))

    # Получите идентификаторы пользователей чата
    chat_users = db.get_chat_users_by_chat_id(chat_id)
    if not chat_users:
        await callback_query.answer("Чат не найден.")
        return

    your_id, user_id = chat_users

    # Удалить чат из базы данных
    db.delete_chat_from_db(your_id, user_id)

    # Обновить список активных чатов
    data = await state.get_data()
    active_chats = data.get('active_chats', [])
    chat_index = data.get('chat_index', 0)

    active_chats = [chat for chat in active_chats if chat['chat_id'] != chat_id]

    if not active_chats:
        await bot.send_message(user_id, "Все чаты были удалены.")
        await state.clear()
    else:
        if chat_index >= len(active_chats):
            chat_index = len(active_chats) - 1

        await state.update_data(active_chats=active_chats, chat_index=chat_index)
        await show_chat(callback_query.message, state, bot)

    await callback_query.answer("Чат удален.")