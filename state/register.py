from aiogram.fsm.state import StatesGroup, State

class RegisterState(StatesGroup):
    regName = State()
    regAge = State()
    regGender = State()
    regGeo = State()