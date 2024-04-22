from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

import app.keyboards as kb
from app.states import Register

router = Router()


# клава всегда цепляется к какому-то апдейту (к отправке сообщения), поэтому цепляем ее
@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Hello!', reply_markup=kb.main_kb)  # привязали клаву к сообщению 'Hello!'. Клава будет открыта
    # await message.reply('How are you?')


@router.message(Command('help'))
async def cmd_help(message: Message):
    await message.answer('Вы нажали на кнопку помощи')


@router.message(F.text == 'QQ')
async def answer_to_qq(message: Message):
    await message.answer(f'И тебе куку {message.from_user.username}!')


@router.message(F.text == 'Каталог')
async def catalog(message: Message):
    await message.answer('Выберите категорию товара', reply_markup=kb.catalog)


# отлавливаем колбэк чтобы среагировать на нажатие кнопки в инлайн клаве
@router.callback_query(F.data == 't-shirts')
async def t_shirt(callback: CallbackQuery):
    await callback.message.answer(
        'Вы бырали категорию футболки')  # ответ будет показан, но кнопка клавы будет активна, что не нужно
    await callback.answer()  # на колбэк всегда нужно отвечать колбэком а не сообщением. Это верный вариант, свечение пропадет
    await callback.answer(show_alert=True)  # более навязчивый ответ с уведомлением


# не всегда может быть достаточно инф-ии о том как обрабатывать сообщения, отвечать на них и добавлять клавиатуру.
# например у нас в боте происходит процесс регистрации, подразумевающий обработку введенных данных, сохранение. И при
# этом другие команды не должны мешать друг другу. Здесь нам и нужен FSM.
@router.message(Command('reg'))
async def register(message: Message, state: FSMContext):
    await state.set_state(Register.name)  # устанавливаем состояние для реагирования
    await message.answer(
        # здесь нужно понять что введено именно имя. Когда юзер выполнит /register, он получит состояние
        'Введите ваше имя'
    )


# этим хендлером ловим состояние 'имя', а не имя юзера
@router.message(Register.name)  # говорим что ловим именно состояние
async def register_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)  # сохр инф-ю(текст юзера) под ключом name
    await state.set_state(Register.age)  # меняем состояние
    await message.answer('Введите возраст')


# этим хендлером ловим состояние 'возраст', а не возраст юзера
@router.message(Register.age)
async def register_age(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    await state.set_state(Register.number)  # меняем состояние
    await message.answer('Введите ваш номер телефона', reply_markup=kb.number)  # привязали клавиатуру для получения номера


# F.contact - если нужно чтобы был отправлен именно как контакт а не текст. Подразумевает наличие клавиатуры для получения номера
@router.message(Register.number, F.contact)
async def register_number(message: Message, state: FSMContext):
    # await state.update_data(number=message.text)
    await state.update_data(number=message.contact.phone_number)  # если хотим чтобы номер контакта сохранился. При message.text будет None
    data = await state.get_data()
    await message.answer(
        f'Ваше имя: {data.get("name")}\nВаш возраст: {data.get("age")}\nВаш номер телефона: {data.get("number")}',
    )
    await state.clear()

















