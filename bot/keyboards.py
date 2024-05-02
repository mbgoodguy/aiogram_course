from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from bot.database.methods.get import get_category_item, get_categories


class Buttontext:
    HELLO = "Hello!"
    WHATS_NEXT = "What's next?"
    BYE = "Bye-bye"
    num_1 = "1⃣"
    COMMANDS = "Команды"
    CONTACTS = "Контакты"


def get_on_startup_kb() -> ReplyKeyboardMarkup:
    button_commands = KeyboardButton(text=Buttontext.COMMANDS)
    button_contacts = KeyboardButton(text=Buttontext.CONTACTS)

    # кнопки в ряд
    buttons_row = [button_commands, button_contacts]
    markup = ReplyKeyboardMarkup(
        keyboard=[buttons_row],
        resize_keyboard=True,
    )

    # кнопки друг под другом
    # button_row_1 = []
    # markup = ReplyKeyboardMarkup(
    #     keyboard=[button_row_1],
    #     # one_time_keyboard=True
    # )
    return markup


# Телефонная клава
def phone_keyboard_builder() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    for i in range(1, 10):
        builder.add(KeyboardButton(text=f'{i}'))  # можно так: builder.button(text=f'{i}')
    builder.button(text='0')
    builder.adjust(3, 3, 3)
    return builder.as_markup()


def phone_keyboard_wo_builder():
    buttons_row1 = [KeyboardButton(text=str(num)) for num in range(1, 4)]
    buttons_row2 = [KeyboardButton(text=str(num)) for num in range(4, 7)]
    buttons_row3 = [KeyboardButton(text=str(num)) for num in range(7, 10)]
    buttons_row4 = [KeyboardButton(text=str(0))]

    markup = ReplyKeyboardMarkup(
        keyboard=[buttons_row1, buttons_row2, buttons_row3, buttons_row4],
        # resize_keyboard=True
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

    return keyboard.adjust(2).as_markup()
