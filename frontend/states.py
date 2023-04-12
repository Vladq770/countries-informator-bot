from aiogram.dispatcher.filters.state import StatesGroup, State


class BotState(StatesGroup):
    choose_name_country = State()
    choose_name_city = State()
    choose_city_from_list = State()
    chosen_country = State()
    chosen_city = State()

