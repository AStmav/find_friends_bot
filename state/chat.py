from aiogram.fsm.state import StatesGroup, State


class ChatStates(StatesGroup):
    active_chat = State()
    chat_index = State()