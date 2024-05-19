import os
from aiogram import Bot
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from utils.database import Database
from handlers.profile import places_all

async def callback_say_hello(call:CallbackQuery,  bot: Bot): # Обработчик нажатия на кнопку "Отправить привет"

    try:
        user_id = int(call.data.split('_')[2])  # ID пользователя, кому отправляем сообщение
        user_id_send = user_id
        print(user_id)
        your_name, your_id = await places_all(call, None, bot)  # Получаем имя отправителя из places_all
        print(your_name, your_id)

        if your_id:
            button_text = 'Начать общение'
            button_data = 'start_chat'
            button_start_chat = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text=button_text, callback_data=button_data)]
            ])
            await bot.send_message(user_id, f"Привет, у вас новое приветственное сообщение от {your_name}\n"
                                             f"Для начала общения нажмите на кнопку:", reply_markup=button_start_chat)
            await call.answer("Приветственное сообщение отправлено!", show_alert=True)

            return user_id_send
        else:
            print("Your ID is not available")
            await call.answer("Не удалось отправить приветственное сообщение.", show_alert=True)
            return None, None
    except IndexError:
        print("IndexError: list index out of range")
        await call.answer("Произошла ошибка при отправке приветственного сообщения.", show_alert=True)
        return None, None
    except Exception as e:
        print(f"An error occurred: {e}")
        await call.answer("Произошла ошибка при отправке приветственного сообщения.", show_alert=True)
        return None, None




