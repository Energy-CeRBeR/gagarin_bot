from copy import deepcopy
from validate_email import validate_email

from aiogram import Router, F
from aiogram.filters import CommandStart, Command, CommandObject, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from messages.messages import USER_MESSAGES, USER_COMMANDS, SECTION_1_QUESTIONS

from database.database import user_db, db_template

from keyboards.keyboards import create_pages_keyboard

from memoryCode.queries import get_token, get_pages, update_page

from states.states import UserSurveyStates, AuthState

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


# Главное меню
@router.message(Command(commands="menu"))
async def to_main_menu(message: Message):
    await message.answer(text=USER_COMMANDS[message.text])


# Хэндлер для просмотра профиля. Если пользователь авторизовался через сайт
# (с помощью почты и пароля от соответствующего сайта), то вывод информации о профиле.
# В противном случае предложить авторизоваться
@router.message(Command(commands="profile"))
async def get_profile_info(message: Message):
    cur_user = user_db[message.from_user.id]
    if cur_user["token"]:
        pages = get_pages(cur_user["token"])
        await message.answer(
            text=USER_COMMANDS[message.text]["with_token"],
            reply_markup=create_pages_keyboard(pages)
        )
    else:
        await message.answer(USER_COMMANDS["no_token"])


# Начало регистрации
@router.message(Command(commands="auth"))
async def start_auth(message: Message, state: FSMContext):
    if not user_db[message.from_user.id]["token"]:
        await message.answer(USER_COMMANDS["auth"]["already_auth"])
    else:
        await message.answer(USER_COMMANDS["auth"]["get_email"])
        await state.set_state(AuthState.get_email)


# Валидация введённой почты, продолжение регистрации
@router.message(AuthState.get_email)
async def continue_auth(message: Message, state: FSMContext):
    user_email = message.text
    if validate_email(user_email):
        user_db[message.from_user.id]["email"] = user_email
        await message.answer(USER_COMMANDS["/auth"]["get_password"])
        await state.set_state(AuthState.get_password)
    else:
        await message.answer(USER_COMMANDS["/auth"]["bad_email"])


@router.message(AuthState.get_password)
async def continue_auth(message: Message, state: FSMContext):
    cur_user = user_db[message.from_user.id]
    user_password = message.text
    user_email = cur_user["email"]
    token = get_token(user_email, user_password)
    if token == "error":
        await message.answer(USER_COMMANDS["/auth"]["invalid_data"])


# Обработка нажатия кнопки для отмены операции
@router.callback_query(F.data == "back")
async def back_button_clicked(callback: CallbackQuery):
    await callback.message.delete()


# Начало опроса
@router.message(StateFilter(None))
async def start_survey(message: Message, state: FSMContext):
    await message.answer(text=USER_MESSAGES['start_survey_section_1'])

    # Задаётся вопрос с нужным индексом
    await message.answer(text=SECTION_1_QUESTIONS[user_db[message.from_user.id]['question_index']])
    user_db[message.from_user.id]['question_index'] += 1

    await state.set_state(UserSurveyStates.survey_section_1)


# Обработка вопросов секции 1
@router.message(UserSurveyStates.survey_section_1)
async def section_1_processing(message: Message, state: FSMContext):
    user_db[message.from_user.id]['section_1_answers'].append(message.text)
    if user_db[message.from_user.id]['question_index'] < len(SECTION_1_QUESTIONS):
        await message.answer(text=SECTION_1_QUESTIONS[user_db[message.from_user.id]['question_index']])
        user_db[message.from_user.id]['question_index'] += 1
