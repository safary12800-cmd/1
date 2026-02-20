from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from filtr.filtr import RoleFilter
from keyboards.reply import register_reply, start_reply, start_reply_admin

router = Router()


@router.message(CommandStart(), RoleFilter("admin"))
async def start_handler_admin(msg: Message):
    await msg.answer(
        "Assalomu alaykum admin, botga xush kelibsiz.\nAdmin panel",
        reply_markup=start_reply_admin(),
    )

   

@router.message(CommandStart())
async def start_handler(msg: Message, db):
    user_name = msg.from_user.full_name if msg.from_user else "Foydalanuvchi"

    if msg.from_user and await db.is_user_exists(msg.from_user.id):
        text = (
            f"Assalomu alaykum, {user_name}.\n"
            "Asosiy menyudan kerakli bo'limni tanlang."
        )
        markup = start_reply()
    else:
        text = (
            f"Assalomu alaykum, {user_name}.\n"
            "Botdan to'liq foydalanish uchun avval registratsiyadan o'ting."
        )
        markup = register_reply()

    await msg.answer(text, reply_markup=markup)
