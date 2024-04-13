from aiogram.fsm.state import StatesGroup, State


class UserSurveyStates(StatesGroup):
    state_1 = State()

    states_list = [f'state_{i}=State()'for i in range(10)]
    for state in states_list:
        exec(state)