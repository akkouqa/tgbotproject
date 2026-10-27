from aiogram.fsm.state import StatesGroup, State


class InputScore(StatesGroup):
    waiting_score = State()
