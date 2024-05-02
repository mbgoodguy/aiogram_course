from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove

import bot.keyboards as kb
from bot.database.methods.get import get_category_name, get_item

router = Router(name=__name__)


@router.message(F.text == 'Dynamic')
async def builder_handler(message: Message):
    await message.answer(
        text='Ты видишь сгенерированную динамически клавиатуру.',
        reply_markup=kb.phone_keyboard_builder()
    )


@router.message(F.text == 'Static')
async def wo_builder_handler(message: Message):
    await message.answer(
        text='Ты видишь статическую клавиатуру.',
        reply_markup=kb.phone_keyboard_wo_builder()
    )


@router.message(F.text == 'Bye-bye')
async def bye_handler(message: Message):
    await message.reply(
        text='Bye-bye! Click /start at any time!',
        reply_markup=ReplyKeyboardRemove()  # скрываем клаву
    )


@router.message(F.text == 'Каталог')
async def catalog_handler(message: Message):
    await message.answer('Выберите категорию товара', reply_markup=await kb.categories())


@router.callback_query(F.data.startswith('category_'))
async def category_handler(callback: CallbackQuery):
    await callback.answer(
        f'Вы выбрали категорию {await get_category_name(int(callback.data.split("_")[-1]))}'
    )
    await callback.message.answer(
        'Выберите товар по категории',
        reply_markup=await kb.items(callback.data.split('_')[1])
    )


@router.callback_query(F.data.startswith('item_'))
async def item_handler(callback: CallbackQuery):
    item = await get_item(int(callback.data.split("_")[-1]))
    # await callback.answer(f'Вы выбрали товар {item.name}')
    await callback.message.answer(
        f'Название: {item.name}\nОписание: {item.description}\nЦена: {item.price} руб.',
        reply_markup=await kb.items(callback.data.split('_')[1])
    )
