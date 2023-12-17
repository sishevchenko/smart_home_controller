from aiogram.fsm.state import StatesGroup, State


class StateConversion(StatesGroup):
    SET_BASE_TARGET_QUANTITY = State()


class StateRates(StatesGroup):
    SET_TARGET = State()
