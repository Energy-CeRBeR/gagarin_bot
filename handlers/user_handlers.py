from copy import deepcopy

from aiogram import Router, F
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.types import Message, CallbackQuery

from messages.messages import USER_MESSAGES, USER_COMMANDS

from database.database import users_db, db_template

from memoryCode import queries

router = Router()


# Обработка команды /start
@router.message(CommandStart())
async def start_bot(message: Message):
    await message.answer(text=USER_COMMANDS[message.text]["in_base"])

    # Проверка, привязал ли пользователь тг к сайту
    if message.from_user.id not in users_db:
        await message.answer(text=USER_COMMANDS[message.text]["no_base"])

    await message.answer(text=USER_COMMANDS[message.text]["in_base"])
