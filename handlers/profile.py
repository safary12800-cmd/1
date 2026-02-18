from aiogram import F, Router
from aiogram.types import Message

router = Router()


@router.message(F.text == "Profile")
async def profile_handler(msg: Message, db):
    if msg.from_user is None:
        await msg.answer("Foydalanuvchi topilmadi.")
        return

    data = await db.user_profile(msg.from_user.id)
    if data is None:
        await msg.answer("Avval ro'yxatdan o'ting.")
        return

    await msg.answer(
        "Profile information:\n"
        f"Ismingiz: {data['name']}\n"
        f"Familyangiz: {data['surename']}\n"
        f"Yoshingiz: {data['age']}\n"
        f"Telefon raqam: {data['phone']}"
    )
