from aiogram import F, Router
from aiogram.types import Message

from keyboards.reply import admin_panel_menu
from filtr.filtr import RoleFilter

router = Router()


@router.message(F.text == "Admin panel", RoleFilter("admin"))
async def admin_panel(msg: Message):
    await msg.answer("Admin panelga xush kelibsiz", reply_markup=admin_panel_menu())
