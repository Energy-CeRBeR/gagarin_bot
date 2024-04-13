from aiogram import Router, F

from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from messages.user_messages import USER_MESSAGES
from messages.survey_messages import SECTION_1_QUESTIONS, SECTION_2_QUESTIONS, INCORRECT_DATE, COMPLETE_SURVEY

from keyboards.keyboards import create_survey_keyboard

from services.services import check_date, get_answers

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

        await state.set_state(UserSurveyStates.get_spouse)
        await message.answer(
            SECTION_2_QUESTIONS[user_db[message.from_user.id]['question_index']],
            reply_markup=create_survey_keyboard()
        )


@router.callback_query(UserSurveyStates.get_spouse, F.data == 'create')
async def create_spouse(callback: CallbackQuery):
    await callback.message.answer('ФИО супруга/супруги')


@router.callback_query(UserSurveyStates.get_spouse, F.data == 'no_create')
async def no_create_spouse(callback: CallbackQuery, state: FSMContext):
    user_db[callback.from_user.id]['section_2_answers'].append('Нет')

    user_db[callback.from_user.id]['question_index'] += 1
    await callback.message.edit_text(
        SECTION_2_QUESTIONS[user_db[callback.from_user.id]['question_index']],
        reply_markup=create_survey_keyboard()
    )

    await state.set_state(UserSurveyStates.get_childrens)


@router.message(UserSurveyStates.get_spouse)
async def write_supouse(message: Message, state: FSMContext):
    user_db[message.from_user.id]['section_2_answers'].append(message.text)

    await state.set_state(UserSurveyStates.get_childrens)

    user_db[message.from_user.id]['question_index'] += 1
    await message.answer(
        SECTION_2_QUESTIONS[user_db[message.from_user.id]['question_index']],
        reply_markup=create_survey_keyboard()
    )


@router.callback_query(UserSurveyStates.get_childrens, F.data == 'create')
async def create_childrens(callback: CallbackQuery):
    await callback.message.answer('ФИО детей')


@router.callback_query(UserSurveyStates.get_childrens, F.data == 'no_create')
async def no_create_spouse(callback: CallbackQuery, state: FSMContext):
    user_db[callback.from_user.id]['section_2_answers'].append('Нет')

    await callback.message.answer(COMPLETE_SURVEY)
    await state.set_state(UserSurveyStates.check_answers)


@router.message(UserSurveyStates.get_childrens)
async def write_supouse(message: Message, state: FSMContext):
    cur_user = user_db[message.from_user.id]
    cur_user['section_2_answers'].append(message.text)
    text = get_answers(cur_user['section_1_answers'], cur_user['section_2_answers'])

    await message.answer(COMPLETE_SURVEY)
    await message.answer(text)
    await state.set_state(UserSurveyStates.check_answers)


@router.message(UserSurveyStates.check_answers)
async def write_answers(message: Message, state: FSMContext):
    pass
