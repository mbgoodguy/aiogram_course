from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.utils import markdown

import app.keyboards as kb
from app.database.requests import get_category_name, get_item

router = Router()


# клава всегда цепляется к какому-то апдейту (к отправке сообщения), поэтому цепляем ее
# @router.message(CommandStart())
# async def cmd_start(message: Message):
#     await rq.set_user(message.from_user.id)
#     await message.answer('Welcome to sneakers store!',
#                          reply_markup=kb.main_kb)  # привязали клаву к сообщению 'Hello!'. Клава будет открыта

@router.message(CommandStart())
async def handle_start(message: Message):
    # в функции обработчике должно быть минимум строк, поэтому лучше вынести кнопки в отдельную ф-ию (пусть будет
    # get_on_startup_kb), которая будет генерировать клавиатуру
    url = 'https://www.cambridge.org/elt/blog/wp-content/uploads/2020/08/GettyImages-1221348467-e1597069527719.jpg'

    await message.answer(
        text=f'{markdown.hide_link(url=url)}Hello, {markdown.text(message.from_user.full_name)}!',
        parse_mode=ParseMode.HTML,
        reply_markup=kb.get_on_startup_kb()
    )


@router.message(F.text == 'Bye-bye')
async def bye_handler(message: Message):
    await message.reply(
        text='Bye-bye! Click /start at any time!',
        reply_markup=ReplyKeyboardRemove()  # скрываем клаву
    )


@router.message(F.text == kb.Buttontext.WHATS_NEXT)
@router.message(Command('help', prefix='!/'))
async def help_handler(message: Message):
    text = markdown.text(
        markdown.markdown_decoration.quote("I'm an echo bot"),
        markdown.text(
            "Send me",
            markdown.markdown_decoration.bold(
                markdown.text(
                    markdown.underline("literally"),
                    "any"
                ),
            ),
            markdown.markdown_decoration.quote('message!')
        ),
        sep='\n'
    )

    await message.answer(
        text=text,
        parse_mode=ParseMode.MARKDOWN_V2,
        reply_markup=kb.get_on_help_kb()
    )


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
