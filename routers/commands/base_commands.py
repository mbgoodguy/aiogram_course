from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from aiogram.utils import markdown

from bot import keyboards as kb

COMMANDS = {
    '/start': 'Старт взаимодействия с ботом',
    '/contacts': 'Получить контакты'
}
router = Router(name=__name__)


@router.message(F.text == 'Команды')
@router.message(Command('commands', prefix='!/'))
async def commands_handler(message: Message):
    commands_text = '\n'.join([f"{command}: {description}" for command, description in COMMANDS.items()])
    await message.answer(
        text=f'Вы можете воспользоваться любой из следующих команд: \n{commands_text}',
    )


@router.message(CommandStart())
async def start_handler(message: Message):
    url = 'https://www.cambridge.org/elt/blog/wp-content/uploads/2020/08/GettyImages-1221348467-e1597069527719.jpg'

    # если хотим ответить фото с подписью
    await message.answer_photo(
        parse_mode=ParseMode.HTML,
        photo=url,
        caption=f'{markdown.hide_link(url=url)}Hello, {markdown.text(message.from_user.full_name)}! '
                f'Твой id: {message.from_user.id}. '
                f'\nВы можете воспользоваться командой /commands для получения информации о доступных командах'
                f' или нажать на кнопку "Команды"',
        reply_markup=kb.get_on_startup_kb()
    )


@router.message(F.text == 'Контакты')
@router.message(Command('contacts', prefix='!/'))
async def contacts_handler(message: Message):
    try:
        with open('texts/contacts.txt', 'r', encoding='utf-8') as file:
            contacts_text = file.read()
        await message.answer(text=contacts_text)
    except FileNotFoundError:
        await message.answer(text="Файл контактов не найден.")
