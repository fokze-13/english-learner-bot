from aiogram.fsm.state import State, StatesGroup


class QuestionFSM(StatesGroup):
    guessing = State()
