from aiogram import Router, F, types

from config import settings

router = Router(name=__name__)


@router.message(F.from_user.id.in_(settings.admin_ids), F.text == 'secret')
async def admin_secret(message: types.Message):
    await message.reply('Чем могу служить, ваше величество?')
