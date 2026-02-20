from aiogram import F,Router
from aiogram.types import Message
from keyboards.reply import admin_panel_menu
from filtr.filtr import RoleFilter
router=Router()

@router.message(F.text=="Admin panel",RoleFilter("Admin"))
async def admin_panel(msg:Message):
    await msg.answer(f'Admin panelga xush kelibsz',reply_markup=admin_panel_menu())