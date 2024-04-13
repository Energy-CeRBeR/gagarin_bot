from copy import deepcopy
from validate_email import validate_email

from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from messages.user_messages import USER_COMMANDS

from database.database import user_db, db_template

from keyboards.keyboards import create_pages_keyboard

from memoryCode.queries import get_token, get_pages, update_page

from states.states import AuthState

router = Router()


@router.message(CommandStart())
async def start_bot(message: Message):
    if message.from_user.id in user_db:
        token = user_db[message.from_user.id]["token"]
        user_db[message.from_user.id] = deepcopy(db_template)
        user_db[message.from_user.id]["token"] = token

    if message.from_user.id not in user_db:
        user_db[message.from_user.id] = deepcopy(db_template)
        await message.answer(text=USER_COMMANDS[message.text]["no_base"])
    else:
        await message.answer(text=USER_COMMANDS[message.text]["in_base"])


# Главное меню
@router.message(Command(commands="menu"))
async def to_main_menu(message: Message):
    if message.from_user.id not in user_db:
        user_db[message.from_user.id] = deepcopy(db_template)

    if message.from_user.id in user_db:
        token = user_db[message.from_user.id]["token"]
        user_db[message.from_user.id] = deepcopy(db_template)
        user_db[message.from_user.id]["token"] = token

    await message.answer(text=USER_COMMANDS[message.text])


@router.callback_query(F.data == "back")
async def back_button_clicked(callback: CallbackQuery):
    await callback.message.delete()


# Начало регистрации
@router.message(Command(commands="auth"))
async def start_auth(message: Message, state: FSMContext):
    if message.from_user.id not in user_db:
        user_db[message.from_user.id] = deepcopy(db_template)

    if message.from_user.id in user_db:
        token = user_db[message.from_user.id]["token"]
        user_db[message.from_user.id] = deepcopy(db_template)
        user_db[message.from_user.id]["token"] = token

    if user_db[message.from_user.id]["token"]:
        await message.answer(USER_COMMANDS[message.text]["already_auth"])
    else:
        await message.answer(USER_COMMANDS[message.text]["get_email"])
        await state.set_state(AuthState.get_email)


@router.message(Command(commands="exit"))
async def exit_from_profile(message: Message):
    user_db[message.from_user.id] = deepcopy(db_template)
    await message.answer("Вы вышли из профиля!")


@router.message(AuthState.get_email)
async def continue_auth(message: Message, state: FSMContext):
    if message.from_user.id not in user_db:
        user_db[message.from_user.id] = deepcopy(db_template)

    user_email = message.text
    if validate_email(user_email):
        user_db[message.from_user.id]["email"] = user_email
        await message.answer(USER_COMMANDS["/auth"]["get_password"])
        await state.set_state(AuthState.get_password)
    else:
        await message.answer(USER_COMMANDS["/auth"]["bad_email"])


# Завершение регистрации
@router.message(AuthState.get_password)
async def continue_auth(message: Message, state: FSMContext):
    if message.from_user.id not in user_db:
        user_db[message.from_user.id] = deepcopy(db_template)

    user_password = message.text
    user_email = user_db[message.from_user.id]["email"]
    token = get_token(user_email, user_password)
    if token == "error":
        await message.answer(USER_COMMANDS["/auth"]["invalid_data"])
    else:
        user_db[message.from_user.id]["token"] = token
        await message.answer(USER_COMMANDS["/auth"]["success_auth"])

    await state.clear()


@router.message(Command(commands="fill_page"))
async def select_page_for_fill(message: Message):
    if message.from_user.id not in user_db:
        user_db[message.from_user.id] = deepcopy(db_template)

    if message.from_user.id in user_db:
        token = user_db[message.from_user.id]["token"]
        user_db[message.from_user.id] = deepcopy(db_template)
        user_db[message.from_user.id]["token"] = token

    cur_user = user_db[message.from_user.id]
    if cur_user["token"]:
        pages = get_pages(cur_user["token"])
        await message.answer(
            text=USER_COMMANDS[message.text]["with_token"],
            reply_markup=create_pages_keyboard(pages, "fill")
        )
    else:
        await message.answer(USER_COMMANDS[message.text]["no_token"])
