from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery

import app.keyboards as kb
from app.database import requests as rq
from app.database.requests import get_category_name, get_item

router = Router()


# клава всегда цепляется к какому-то апдейту (к отправке сообщения), поэтому цепляем ее
@router.message(CommandStart())
async def cmd_start(message: Message):
    await rq.set_user(message.from_user.id)
    await message.answer('Welcome to sneakers store!',
                         reply_markup=kb.main_kb)  # привязали клаву к сообщению 'Hello!'. Клава будет открыта


@router.message(F.text == 'Каталог')
async def catalog(message: Message):
    await message.answer('Выберите категорию товара', reply_markup=await kb.categories())


@router.callback_query(F.data.startswith('category_'))
async def category(callback: CallbackQuery):
    await callback.answer(
        f'Вы выбрали категорию {await get_category_name(int(callback.data.split("_")[-1]))}'
    )
    await callback.message.answer(
        'Выберите товар по категории',
        reply_markup=await kb.items(callback.data.split('_')[1])
    )


@router.callback_query(F.data.startswith('item_'))
async def item(callback: CallbackQuery):
    item = await get_item(int(callback.data.split("_")[-1]))
    # await callback.answer(f'Вы выбрали товар {item.name}')
    await callback.message.answer(
        f'Название: {item.name}\nОписание: {item.description}\nЦена: {item.price} руб.',
        reply_markup=await kb.items(callback.data.split('_')[1])
    )
