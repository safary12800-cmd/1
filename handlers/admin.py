from aiogram import F, Router
from aiogram.types import Message,CallbackQuery

from keyboards.reply import admin_panel_menu, start_reply_admin
from keyboards.inline import users_inline,role_inline
from filtr.filtr import RoleFilter

router = Router()


@router.message(F.text == "Admin panel", RoleFilter("admin"))
async def admin_panel(msg: Message):
    await msg.answer("Admin panelga xush kelibsiz", reply_markup=admin_panel_menu())

    await msg.answer(f'Admin panelga xush kelibsz',reply_markup=admin_panel_menu())


@router.message(F.text.in_({"⬅️ Orqaga", "Orqaga"}), RoleFilter("admin"))
async def back_to_admin_menu(msg: Message):
    await msg.answer("Asosiy admin menyu", reply_markup=start_reply_admin())

@router.message(F.text==("👥 Userlar"), RoleFilter("Admin"))
async def show_users(message: Message, db):
    users = await db.get_users()

    if not users:
        await message.answer("Userlar yoq")
        return

    await message.answer(
        "👥 Userlar royxati:",
        reply_markup=users_inline(users)
    )

@router.callback_query(F.data.startswith("user_"),RoleFilter("Admin"))
async def choose_role(callback: CallbackQuery):
    if callback.data is None:
        return
    telegram_id = int(callback.data.split("_")[1]) 

    if callback.message is not None:
        await callback.message.answer("🔄 Role tanlang:",reply_markup=role_inline(telegram_id))
    await callback.answer()

@router.callback_query(lambda c: c.data.startswith("setrole_"),RoleFilter("Admin"))
async def set_role(callback: CallbackQuery, db):
    await new_func(callback, db)

async def new_func(callback, db):
    _, role, telegram_id = callback.data.split("_")

    await db.set_user_role(
        telegram_id=int(telegram_id),
        role=role
    )

    await callback.message.edit_text(
        f"✅ User roli `{role}` ga o‘zgartirildi"
    )
    await callback.answer("Role yangilandi")
