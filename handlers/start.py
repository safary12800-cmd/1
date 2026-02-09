from aiogram.filters import CommandStart
from aiogram import Router
from aiogram.types import Message
from keyboards.reply import start_reply,register_reply

router=Router()

@router.message(CommandStart())
async def start_handler(msg:Message):
    user_name = msg.from_user.full_name if msg.from_user else "Foydalanuvchi"
    await msg.answer(f"Assalomu Alaykum {user_name}, botga xush kelibsiz", reply_markup=register_reply())