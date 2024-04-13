from copy import deepcopy

from aiogram import Router, F
from aiogram.filters import CommandStart, Command, CommandObject, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from messages.messages import USER_MESSAGES, USER_COMMANDS

from database.database import user_db, db_template

from memoryCode import queries

from states.user_survey_states import UserSurveyStates

router = Router()


number_q = 0


# Обработка команды /start
@router.message(CommandStart())
async def start_bot(message: Message):
    await message.answer(text=USER_COMMANDS[message.text]["in_base"])

    # Проверка, привязал ли пользователь тг к сайту
    if message.from_user.id not in user_db:
        user_db[message.from_user.id] = deepcopy(db_template)
        await message.answer(text=USER_COMMANDS[message.text]["no_base"])

    await message.answer(text=USER_COMMANDS[message.text]["in_base"])


# Хэндлер для просмотра профиля. Если пользователь авторизовался через сайт
# (с помощью почты и пароля от соответствующего сайта), то вывод информации о профиле.
# В противном случае предложить авторизоваться
@router.message(Command(commands="profile"))
async def get_profile_info(message: Message):
    pass


# Начало опроса
@router.message(StateFilter(None))
async def start_survey(message: Message, state: FSMContext):
    await state.set_state

    await message.answer(text='Стейт поставлен.')


@router.message(UserSurveyStates.question_1)
async def start_survey(message: Message, state: FSMContext):
    await message.answer(text='стейт 1')