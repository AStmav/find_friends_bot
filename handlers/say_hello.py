import os
from aiogram import Bot
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from utils.database import Database
from handlers.profile import places_all


async def callback_say_hello(call:CallbackQuery, state: FSMContext, bot: Bot): # Обработчик нажатия на кнопку "Отправить привет"

    try:
        user_id = int(call.data.split('_')[2])  # ID пользователя, кому отправляем сообщение
        print(f"кому приходит сообщение {user_id}")

        # Получаем ID пользователя, который инициировал поиск, из состояния FSMContext
        state_data = await state.get_data()
        seeker_id = state_data.get('seeker_id')
        print(f" а почлучил это {seeker_id}")

        if seeker_id:
            db = Database(os.getenv('DATABASE_NAME'))
            user_data = db.select_users_id(seeker_id)
            if not user_data:
                print("Seeker user data not found")
                await call.answer("Не удалось определить пользователя, инициировавшего поиск.", show_alert=True)
                return

            your_name = user_data[1]  # Имя отправителя
            your_id = seeker_id  # ID отправителя
            print(f"Имя и ид того кто создает чат {your_name}, {your_id}")

            # Проверка, существует ли уже сессия чата
            if db.check_existing_chat(your_id, user_id):
                print("Chat session already exists")
                await bot.send_message(call.from_user.id, "Чат с этим пользователем уже существует.")
                await call.answer("Чат с этим пользователем уже существует.", show_alert=True, )
                return

            db.save_user_id_chat(your_id, user_id)
            button_text = 'Начать общение'
            button_data = 'start_chat'
            button_start_chat = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text=button_text, callback_data=button_data)]
            ])
            await bot.send_message(user_id, f"Привет, у вас новое приветственное сообщение от {your_name}\n"
                                            f"Для начала общения нажмите на кнопку:",
                                   reply_markup=button_start_chat)
            await call.answer("Приветственное сообщение отправлено!", show_alert=True)

            return user_id
        else:
            print("Seeker ID is not available")
            await call.answer("Не удалось определить пользователя, инициировавшего поиск.", show_alert=True)
            return None
    except IndexError:
        print("IndexError: list index out of range")
        await call.answer("Произошла ошибка при отправке приветственного сообщения.", show_alert=True)
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        await call.answer("Произошла ошибка при отправке приветственного сообщения.", show_alert=True)
        return None


