import asyncio
import logging

from aiogram import Dispatcher, Bot

from bot.database.engine import async_main
from config import settings
from routers import router as main_router


async def main():
    logging.basicConfig(level=logging.INFO)
    await async_main()
    bot = Bot(token=settings.bot_token)
    dp = Dispatcher()
    dp.include_router(main_router)

    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот выключен')
