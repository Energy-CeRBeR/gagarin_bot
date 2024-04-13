from aiogram import Router, F

from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from messages.user_messages import USER_MESSAGES
from messages.survey_messages import SECTION_1_QUESTIONS, SECTION_2_QUESTIONS, INCORRECT_DATE, COMPLETE_SURVEY

from keyboards.keyboards import create_survey_keyboard, create_show_keyboard, create_yes_no_keyboard

from yaGPT.queries import get_epitaph, get_biography
from memoryCode.queries import update_page

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

    await state.set_state(UserSurveyStates.get_children)


@router.message(UserSurveyStates.get_spouse)
async def write_supouse(message: Message, state: FSMContext):
    user_db[message.from_user.id]['section_2_answers'].append(message.text)

    await state.set_state(UserSurveyStates.get_children)

    user_db[message.from_user.id]['question_index'] += 1
    await message.answer(
        SECTION_2_QUESTIONS[user_db[message.from_user.id]['question_index']],
        reply_markup=create_survey_keyboard()
    )


@router.callback_query(UserSurveyStates.get_children, F.data == 'create')
async def create_children(callback: CallbackQuery):
    await callback.message.answer('ФИО детей')


@router.callback_query(UserSurveyStates.get_children, F.data == 'no_create')
async def no_create_spouse(callback: CallbackQuery, state: FSMContext):
    user_db[callback.from_user.id]['section_2_answers'].append('Нет')

    await callback.message.edit_text(
        text=COMPLETE_SURVEY,
        reply_markup=create_show_keyboard()
    )
    await state.clear()


@router.message(UserSurveyStates.get_children)
async def get_children_name(message: Message, state: FSMContext):
    user_db[message.from_user.id]['section_2_answers'].append(message.text)

    await message.answer(
        text=COMPLETE_SURVEY,
        reply_markup=create_show_keyboard()
    )

    await state.clear()


@router.callback_query(F.data == "show_results")
async def show_results(callback: CallbackQuery):
    cur_user = user_db[callback.from_user.id]

    text = get_answers(cur_user['section_1_answers'], cur_user['section_2_answers'])

    await callback.message.answer(text)
    await callback.message.answer(
        text="Заполнить поля с биографией и эпитафией?",
        reply_markup=create_yes_no_keyboard("show")
    )


@router.callback_query(F.data == "show_YES" or F.data == "show_NO")
async def fill_data(callback: CallbackQuery):
    cur_user = user_db[callback.from_user.id]
    section_1 = cur_user["section_1_answers"]
    section_2 = cur_user["section_2_answers"]
    AI_biography = "Не сгенерировано"
    AI_epitaph = "Не сгенерировано"

    if callback.data == "NO":
        await callback.message.delete()
        await callback.message.answer("Всё готово к отправке на сайт!")
    else:
        await callback.message.delete()

        info = section_1[:5] + section_2 + section_1[6:9]

        try:
            AI_epitaph = get_epitaph(info)
        except KeyError:
            ...
        user_db[callback.from_user.id]["epitaph"] = AI_epitaph

        try:
            AI_biography = get_biography(info)
        except KeyError:
            ...
        user_db[callback.from_user.id]["biography"] = AI_biography

        text = (f"Эпитафия:\n"
                f"{AI_epitaph}\n\n"
                f"Биография:\n"
                f"{AI_biography}")

        await callback.message.answer(text)

    await callback.message.answer("Данные отправляются на сайт. Пожалуйста, подождите!")
    update_page(cur_user["token"], cur_user["cur_page_slug"], AI_epitaph, AI_biography, section_1, section_2)
    await callback.message.answer("Данные успешно загружены!")
