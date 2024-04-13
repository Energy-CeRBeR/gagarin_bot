from aiogram import Router, F

from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from messages.user_messages import USER_MESSAGES
from messages.survey_messages import SECTION_1_QUESTIONS, SECTION_2_QUESTIONS, INCORRECT_DATE, COMPLETE_SURVEY

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
    else:
        user_db[message.from_user.id]['question_index'] = 0

        await message.answer('as')
        await state.set_state(UserSurveyStates.get_spouse)
        await message.answer(SECTION_2_QUESTIONS[user_db[message.from_user.id]['question_index']][0], reply_markup=SECTION_2_QUESTIONS[user_db[message.from_user.id]['question_index']][1])


@router.callback_query(UserSurveyStates.get_spouse, F.data == 'create')
async def create_spouse(callback: CallbackQuery):
    await callback.message.answer('ФИО супруга/супруги')


@router.callback_query(UserSurveyStates.get_spouse, F.data == 'no_creat')
async def no_create_spouse(callback: CallbackQuery, state: FSMContext):
    user_db[callback.message.from_user.id]['section_2_answers'].append('Нет')

    user_db[callback.message.from_user.id]['question_index'] += 1
    await callback.message.answer(await callback.message.answer(SECTION_2_QUESTIONS[user_db[callback.message.from_user.id]['question_index']][0], reply_markup=SECTION_2_QUESTIONS[user_db[callback.message.from_user.id]['question_index']][1]))

    await state.set_state(UserSurveyStates.get_childrens)


@router.message(UserSurveyStates.get_spouse)
async def write_supouse(message: Message, state: FSMContext):
    user_db[message.from_user.id]['section_2_answers'].append(message.text)

    await state.set_state(UserSurveyStates.get_childrens)

    user_db[message.from_user.id]['question_index'] += 1
    await message.answer(await message.answer(SECTION_2_QUESTIONS[user_db[message.from_user.id]['question_index']][0], reply_markup=SECTION_2_QUESTIONS[user_db[message.from_user.id]['question_index']][1]))


@router.callback_query(UserSurveyStates.get_childrens, F.data == 'create')
async def create_childrens(callback: CallbackQuery):
    await callback.message.answer('ФИО детей')


@router.callback_query(UserSurveyStates.get_childrens, F.data == 'no_creat')
async def no_create_spouse(callback: CallbackQuery, state: FSMContext):
    user_db[callback.message.from_user.id]['section_2_answers'].append('Нет')

    await callback.message.answer(COMPLETE_SURVEY)
    await state.clear()


@router.message(UserSurveyStates.get_childrens)
async def write_supouse(message: Message, state: FSMContext):
    user_db[message.from_user.id]['section_2_answers'].append(message.text)

    await message.answer(COMPLETE_SURVEY)
    await state.clear()
