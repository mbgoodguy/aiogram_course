import asyncio
import os

from aiogram import Dispatcher, Bot
from dotenv import load_dotenv

from bot.database.engine import async_main
from bot.handlers import router

load_dotenv()


async def main():
    await async_main()
    bot = Bot(token=os.getenv('TOKEN'))
    dp = Dispatcher()
    dp.include_router(router)

    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот выключен')
