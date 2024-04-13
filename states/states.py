from aiogram.fsm.state import StatesGroup, State


class AuthState(StatesGroup):
    get_email = State()
    get_password = State()


class UserSurveyStates(StatesGroup):
    # Простые вопросы с короткими ответами
    survey_section_1 = State()

    # Вопросы с выбором варианта
    survey_section_2 = State()


class GlobalStates(StatesGroup):
    new_page = State()