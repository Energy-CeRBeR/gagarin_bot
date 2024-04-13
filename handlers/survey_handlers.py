from aiogram import Router, F

from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from messages.user_messages import USER_MESSAGES
from messages.survey_messages import SECTION_1_QUESTIONS, INCORRECT_DATE

from services.services import check_date

from database.database import user_db

from states.states import UserSurveyStates

router = Router()


# Начало опроса
@router.callback_query(F.data[:9] == "fill_page")
async def start_survey(callback: CallbackQuery, state: FSMContext):
    user_db[callback.from_user.id]["cur_page_slug"] = int(callback.data[9:])

    await callback.message.answer(text=USER_MESSAGES['start_survey_section_1'])

    # Задаётся вопрос с нужным индексом
    await callback.message.answer(text=SECTION_1_QUESTIONS[user_db[callback.from_user.id]['question_index']])
    user_db[callback.from_user.id]['question_index'] += 1

    await state.set_state(UserSurveyStates.survey_section_1)


@router.message(UserSurveyStates.survey_section_1)
async def section_1_processing(message: Message, state: FSMContext):
    user_db[message.from_user.id]['section_1_answers'].append(message.text)
    if user_db[message.from_user.id]['question_index'] < len(SECTION_1_QUESTIONS):
        if "Дата" in SECTION_1_QUESTIONS[user_db[message.from_user.id]['question_index'] - 1]:
            if check_date(message.text):
                await message.answer(text=SECTION_1_QUESTIONS[user_db[message.from_user.id]['question_index']])
                user_db[message.from_user.id]['question_index'] += 1
            else:
                await message.answer(INCORRECT_DATE)
        else:
            await message.answer(text=SECTION_1_QUESTIONS[user_db[message.from_user.id]['question_index']])
            user_db[message.from_user.id]['question_index'] += 1
