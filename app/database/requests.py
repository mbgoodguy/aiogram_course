from sqlalchemy import select

from app.database.models import User, async_session, Category, Item


async def set_user(tg_id):
    async with async_session() as db:
        user = await db.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            db.add(User(tg_id=tg_id))  # не возвращает корутину, то есть не awaitable, поэтому без await
            await db.commit()


async def get_categories():
    async with async_session() as db:
        return await db.scalars(select(Category))


async def get_category_name(id: int):
    async with async_session() as db:
        category = await db.scalar(select(Category).where(Category.id == id))
        return category.name


async def get_category_item(category_id: int):
    async with async_session() as db:
        return await db.scalars(select(Item).where(Item.category == category_id))


async def get_item(item_id: int):
    async with async_session() as db:
        item = await db.scalar(select(Item).where(Item.id == item_id))
        return item
