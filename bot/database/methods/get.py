from sqlalchemy import select

from bot.database.engine import async_session
from bot.database.models import Category, Item


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


async def get_categories():
    async with async_session() as db:
        return await db.scalars(select(Category))
