from sqlalchemy import select

from bot.database.models import User
from bot.database.engine import async_session


async def set_user(tg_id):
    async with async_session() as db:
        user = await db.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            db.add(User(tg_id=tg_id))  # не возвращает корутину, то есть не awaitable, поэтому без await
            await db.commit()
