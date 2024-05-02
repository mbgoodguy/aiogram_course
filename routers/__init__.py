__all__ = ("router",)

from aiogram import Router

from routers.admin_handlers import router as admin_router
from routers.common import router as common_router
from .commands import router as commands_router

router = Router(name=__name__)  # этот роутер нужно подключить в main.py

router.include_routers(
    commands_router,
    admin_router,
)

# Должен идти последним, т.к порядок обработчиков важен
router.include_router(common_router)
