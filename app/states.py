from aiogram.fsm.state import State, StatesGroup


class Register(StatesGroup):
    interval = State()
    tags = State()
