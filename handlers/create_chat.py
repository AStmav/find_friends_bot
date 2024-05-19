from aiogram import Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from utils.database import Database
from handlers.profile import places_all
from handlers.say_hello import callback_say_hello
from state.create_chat import CreateChatState

async def start_chat_friends(call:CallbackQuery, bot:Bot, state: FSMContext): #Обработка нажатия на кнопку "начать общение"
    try:
        your_id = await places_all(call, state, bot)
        user_id_send= await callback_say_hello(call, bot)
        #your_id = 1320680053
        #user_id = 1787078931

        if your_id and user_id_send:
            # await CreateChatState.CreateChat.set()
            await state.update_data(user_id=user_id_send, your_id=your_id)
            await state.set_state(CreateChatState.CreateChat)
            await call.message.answer("Чат успешно создан!")
        else:
            print("Failed to start chat")
            await call.answer("Не удалось начать чат.", show_alert=True)
    except Exception as e:
        print(f"An error occurred: {e}")
        await call.answer("Произошла ошибка при начале чата.", show_alert=True)

