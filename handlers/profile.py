from aiogram import F, Router
from aiogram.types import Message

from keyboards.reply import register_reply

router = Router()


@router.message(F.text == "Profile")
async def profile_handler(msg: Message, db):
    if msg.from_user is None:
        await msg.answer(
            "Profilni ko'rish uchun avval registratsiyadan o'ting.",
            reply_markup=register_reply(),
        )
        return

    user = await db.get_user_by_telegram_id(msg.from_user.id)
    if user is None:
        await msg.answer(
            "Profil topilmadi. Avval registratsiyadan o'ting.",
            reply_markup=register_reply(),
        )
        return

    await msg.answer(
        text=(
            "Sizning profilingiz\n\n"
            f"Telegram ID: {user['telegram_id']}\n"
            f"Ism: {user['name']}\n"
            f"Familiya: {user['surename']}\n"
            f"Yosh: {user['age']}\n"
            f"Telefon: {user['phone']}\n"
            f"Rol: {user['role']}"
        )
    )
