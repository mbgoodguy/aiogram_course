from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from bot.database.models import Base


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


engine = create_async_engine(url='sqlite+aiosqlite:///db.sqlite3')
async_session = async_sessionmaker(engine)
