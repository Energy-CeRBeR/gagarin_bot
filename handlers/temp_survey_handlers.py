from copy import deepcopy

from aiogram import Router, F
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from messages.messages import USER_MESSAGES, USER_COMMANDS
from messages.messages_questions import SECTION_1_QUESTIONS, ERROR_MESSAGE

from .check_date import check_date # Проверка на корректность введённой даты

from database.database import user_db, db_template

from states.states import UserSurveyStates

router = Router()


@router.message(CommandStart())
async def start_bot(message: Message):
    # Проверка, привязал ли пользователь тг к сайту
    if message.from_user.id not in user_db:
        user_db[message.from_user.id] = deepcopy(db_template)
        await message.answer(text=USER_COMMANDS[message.text]["no_base"])
    else:
        await message.answer(text=USER_COMMANDS[message.text]["in_base"])


@router.message(StateFilter(None))
async def start_survey(message: Message, state: FSMContext):
    await message.answer(text=USER_MESSAGES['start_survey_section_1'])

    # Задаётся вопрос с нужным индексом
    await message.answer(text=SECTION_1_QUESTIONS[user_db[message.from_user.id]['question_index']])

    await state.set_state(UserSurveyStates.survey_section_1)


# Обработка вопросов секции 1
@router.message(UserSurveyStates.survey_section_1)
async def section_1_processing(message: Message, state: FSMContext):
    if 'Дата' in SECTION_1_QUESTIONS[user_db[message.from_user.id]['question_index']]:
        if not check_date(message.text):
            await message.answer(ERROR_MESSAGE)
            return True

    await message.answer('ок')
    user_db[message.from_user.id]['section_1_answers'].append(message.text)

    user_db[message.from_user.id]['question_index'] += 1
    if user_db[message.from_user.id]['question_index'] < len(SECTION_1_QUESTIONS):
        await message.answer(text=SECTION_1_QUESTIONS[user_db[message.from_user.id]['question_index']])

        user_db[message.from_user.id]['question_index'] += 1
