from aiogram import Router
from aiogram.exceptions import TelegramAPIError
from aiogram.filters import CommandStart
from aiogram.types import Message

from config import config
from keyboards.reply import register_reply, start_reply

router = Router()


async def _send_sticker_safe(msg: Message, sticker_id: str):
    if not sticker_id:
        return
    try:
        await msg.answer_sticker(sticker_id)
    except TelegramAPIError:
        pass


@router.message(CommandStart())
async def start_handler(msg: Message, db):
    user_name = msg.from_user.full_name if msg.from_user else "Foydalanuvchi"
    await _send_sticker_safe(msg, config.START_STICKER_ID)

    if msg.from_user and await db.is_user_exists(msg.from_user.id):
        markup = start_reply()
        text = (
            f"Assalomu alaykum, {user_name}.\n"
            "Kerakli bo'limni menyudan tanlang."
        )
    else:
        markup = register_reply()
        text = (
            f"Assalomu alaykum, {user_name}.\n"
            "Davom etish uchun Register tugmasini bosing."
        )

    await msg.answer(text, reply_markup=markup)
