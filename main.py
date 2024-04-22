import asyncio

from aiogram import Dispatcher, Bot

from app.handlers import router


async def main():
    bot = Bot(token='7042810299:AAGoGwSAgH54NJGL55ei_YYIkTguS-SIzzQ')
    dp = Dispatcher()
    dp.include_router(router)

    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот выключен')
