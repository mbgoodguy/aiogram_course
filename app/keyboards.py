from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.database.requests import get_categories, get_category_item


class Buttontext:
    HELLO = "Hello!"
    WHATS_NEXT = "What's next?"
    BYE = "Bye-bye"
    num_1 = "1⃣"


def get_on_startup_kb():
    button_hello = KeyboardButton(text=Buttontext.HELLO)
    button_help = KeyboardButton(text=Buttontext.WHATS_NEXT)
    button_bye = KeyboardButton(text=Buttontext.BYE)

    # кнопки в ряд
    # buttons_row = [button_help, button_hello]
    # markup = ReplyKeyboardMarkup(keyboard=[buttons_row])

    # кнопки друг под другом
    button_row_1 = [button_hello, button_help]
    button_row_2 = [button_bye]
    markup = ReplyKeyboardMarkup(
        keyboard=[button_row_1, button_row_2],
        # one_time_keyboard=True
    )

    return markup


def get_on_help_kb():
    emoji_nums = [
        "0⃣",
        "1⃣",
        "2⃣",
        "3⃣",
        "4⃣",
        "5⃣",
        "6⃣",
        "7⃣",
        "8⃣",
        "9⃣",
    ]
    buttons_row = [KeyboardButton(text=num) for num in emoji_nums]
    buttons_row.append(buttons_row[0])  # добавляет в конец строки
    buttons_row.append(buttons_row[1])  # добавляет в конец строки
    buttons_row.append(buttons_row[2])  # не увидим, т.к лимит эл-ов в строке 12
    buttons_row.pop(0)  # удалили 0
    buttons_row.append(buttons_row[2])  # увидим, т.к удалили последний эл-т и добавили новый

    '''
    Лучше придерживаться 3-5 элементов в строке и делать больше строк, если нужно, а не элементов в строке. Потому что
    мы можем строки проскроллить вертикально, а горизонтальной прокрутки нет. И вот когда мы такие клавы используем,
    пригодится KeyboardBuilder
    '''

    markup = ReplyKeyboardMarkup(
        keyboard=[buttons_row, buttons_row],
        resize_keyboard=True
    )

    return markup


main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Каталог')],
        [KeyboardButton(text='Корзина')],
        [KeyboardButton(text='Контакты'), KeyboardButton(text='О нас')],
    ],
    resize_keyboard=True,
    input_field_placeholder='Выбери пункт меню...'
)


async def categories():
    all_categories = await get_categories()
    keyboard = InlineKeyboardBuilder()

    for category in all_categories:
        keyboard.add(InlineKeyboardButton(text=category.name, callback_data=f'category_{category.id}'))
    keyboard.add(InlineKeyboardButton(text='На главную', callback_data='to_main'))

    return keyboard.adjust(3).as_markup()  # as_markup всегда исп-ем когда исп-ем Builder чтобы превратить его в клаву


async def items(category_id):
    all_items = await get_category_item(category_id)
    keyboard = InlineKeyboardBuilder()

    for item in all_items:
        keyboard.add(InlineKeyboardButton(text=item.name, callback_data=f'item_{item.id}'))
    keyboard.add(InlineKeyboardButton(text='На главную', callback_data='to_main'))

    return keyboard.adjust(2).as_markup()  # as_markup всегда исп-ем когда исп-ем Builder чтобы превратить его в клаву
