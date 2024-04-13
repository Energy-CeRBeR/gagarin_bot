import asyncio

from aiogram import Dispatcher, Bot
from config_data.config import Config, load_config

from handlers.user_handlers import router as user_router
from handlers.temp_survey_handlers import router as survey_router

'''
В данном модуле происходит выгрузка данных из .env, подключение всех роутеров, запуск бота
'''


async def main():
    config: Config = load_config(".env")
    bot = Bot(token=config.tg_bot.token)
    dp = Dispatcher()

    dp.include_router(user_router)
    # dp.include_router(survey_router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
