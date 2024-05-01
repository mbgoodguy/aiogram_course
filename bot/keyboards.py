from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from bot.database.methods.get import get_category_item, get_categories


class Buttontext:
    HELLO = "Hello!"
    WHATS_NEXT = "What's next?"
    BYE = "Bye-bye"
    num_1 = "1⃣"
    HELP = "Help"


def get_on_startup_kb() -> ReplyKeyboardMarkup:
    # button_hello = KeyboardButton(text=Buttontext.HELLO)
    button_help = KeyboardButton(text=Buttontext.WHATS_NEXT)
    button_bye = KeyboardButton(text=Buttontext.BYE)

    # кнопки в ряд
    # buttons_row = [button_help, button_hello]
    # markup = ReplyKeyboardMarkup(keyboard=[buttons_row])

    # кнопки друг под другом
    button_row_1 = [button_help, button_bye]
    markup = ReplyKeyboardMarkup(
        keyboard=[button_row_1],
        # one_time_keyboard=True
    )

    return markup


# def get_on_help_kb():
#     emoji_nums = [
#         "1⃣",
#         "2⃣",
#         "3⃣",
#         "4⃣",
#         "5⃣",
#         "6⃣",
#         "7⃣",
#         "8⃣",
#         "9⃣",
#         "0⃣",
#     ]
#     buttons_row = [KeyboardButton(text=num) for num in emoji_nums]
#     # buttons_row.append(buttons_row[0])  # добавляет в конец строки
#     # buttons_row.append(buttons_row[1])  # добавляет в конец строки
#     # buttons_row.append(buttons_row[2])  # не увидим, т.к лимит эл-ов в строке 12
#     # buttons_row.pop(0)  # удалили 0
#     # buttons_row.append(buttons_row[2])  # увидим, т.к удалили последний эл-т и добавили новый
#
#     # markup = ReplyKeyboardMarkup(
#     #     keyboard=[buttons_row, buttons_row],
#     #     resize_keyboard=True
#     # )
#     #
#     # return markup
#
#     '''
#     Лучше придерживаться 3-5 элементов в строке и делать больше строк, если нужно, а не элементов в строке. Потому что
#     мы можем строки проскроллить вертикально, а горизонтальной прокрутки нет. И вот когда мы такие клавы используем,
#     пригодится KeyboardBuilder
#     '''
#
#     builder = ReplyKeyboardBuilder()
#
#     for num in emoji_nums:
#         # builder.button(text=num)  # button просто генерирует кнопку автоматически. Но мы можем и создать кнопку и
#         # через метод add куда передать KeyboardButton
#         builder.add(KeyboardButton(text=num))  # сюда можем передать несколько кнопок, каждая будет добавлена в строку,
#         # если лимит строки не достигнут
#
#     # builder.adjust(3).as_markup(resize_keyboard=True)  # установка 3 кнопок в ряд
#     builder.adjust(3, 3, 4).as_markup(resize_keyboard=True)  # в первом 3, во втором 3, в последнем 4
#
#     # добавление
#     builder.add(KeyboardButton(text='Q'))  # add добавляет в конец строки. Переносит кнопки на новый ряд если достигнут лимит ширины (10)
#     builder.row(buttons_row[-1], buttons_row[-2])  # добавляем новую строку в билдер. Всегда добавление на новую строку
#
#     builder.row(buttons_row[-3])  # 8
#
#     builder.row(buttons_row[1])
#     builder.add(buttons_row[2])
#     builder.add(buttons_row[3])
#
#     builder.row(KeyboardButton(text='Кнопка добавленная через row'))
#
#     return builder.as_markup()  # если не укажем as_markup, то будет ошибка reply_markup.ForceReply


def get_contacts_kb():
    markup = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text='Контакты'),
            ]
        ]
    )

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

    return keyboard.adjust(2).as_markup()  # as_markup всегда исп-ем когда исп-ем Builder чтобы превратить его в клаву
