from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Каталог')],  #  здесь м ыхотим чтобы появилась инлйн клавиатура при нажатии на Каталог
        [KeyboardButton(text='Корзина')],
        [KeyboardButton(text='Контакты'), KeyboardButton(text='О нас')],
    ],
    resize_keyboard=True,
    input_field_placeholder='Выбери пункт меню...'
)


# инлайн клава не может быть создана с текстом, т.к текст не отправляется в чат. Нужно как-то понять что мы отправили
# сообщение. Для этого добавляем callback_data
catalog = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Футболки', callback_data='t-shirts')],
        [InlineKeyboardButton(text='Кроссовки', callback_data='sneakers')],
        [InlineKeyboardButton(text='Кепки', callback_data='caps')],
    ]
)


number = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Отправить контакт', request_contact=True)]
    ],
    resize_keyboard=True
)
