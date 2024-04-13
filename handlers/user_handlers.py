from copy import deepcopy

from aiogram import Router, F
from aiogram.filters import CommandStart, Command, CommandObject, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from messages.messages import USER_MESSAGES, USER_COMMANDS, SECTION_1_QUESTIONS

from database.database import user_db, db_template

from memoryCode import queries

from states.user_survey_states import UserSurveyStates
from states.global_states import GlobalStates

router = Router()


# Обработка команды /start
@router.message(CommandStart())
async def start_bot(message: Message):
    # Проверка, привязал ли пользователь тг к сайту
    if message.from_user.id not in user_db:
        user_db[message.from_user.id] = deepcopy(db_template)
        await message.answer(text=USER_COMMANDS[message.text]["no_base"])
    else:
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
    await message.answer(text=USER_MESSAGES['start_survey_section_1'])

    # Задаётся вопрос с нужным индексом
    await message.answer(text=SECTION_1_QUESTIONS[user_db[message.from_user.id]['question_index']])
    user_db[message.from_user.id]['question_index'] += 1

    await state.set_state(UserSurveyStates.survey_section_1)


# Обработа вопросов секции 1
@router.message(UserSurveyStates.survey_section_1)
async def section_1_processing(message: Message, state: FSMContext):
    user_db[message.from_user.id]['section_1_answers'].append(message.text)
    if user_db[message.from_user.id]['question_index'] < len(SECTION_1_QUESTIONS):
        await message.answer(text=SECTION_1_QUESTIONS[user_db[message.from_user.id]['question_index']])
        user_db[message.from_user.id]['question_index'] += 1
