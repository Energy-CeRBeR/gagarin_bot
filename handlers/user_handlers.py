from aiogram import Router, F
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.types import Message, CallbackQuery

router = Router()


@router.message(CommandStart())
async def start_bot(message: Message):
    pass
