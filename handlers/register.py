from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from keyboards.reply import register_phone_reply, register_reply, start_reply
from states.register import RegisterState

router = Router()

CANCEL_TEXT = "Bekor qilish"


def _normalize_phone(raw_phone: str) -> str:
    cleaned = "".join(ch for ch in raw_phone if ch.isdigit() or ch == "+")
    if not cleaned:
        return ""

    if not cleaned.startswith("+"):
        digits = "".join(ch for ch in cleaned if ch.isdigit())
        cleaned = f"+{digits}"

    return cleaned


def _is_valid_phone(phone: str) -> bool:
    digits = "".join(ch for ch in phone if ch.isdigit())
    return 9 <= len(digits) <= 15


@router.message(F.text == "Register")
async def register_start(msg: Message, state: FSMContext, db):
    if msg.from_user and await db.is_user_exists(msg.from_user.id):
        await msg.answer(
            "Siz allaqachon registratsiyadan o'tib bo'lgansiz.",
            reply_markup=start_reply(),
        )
        await state.clear()
        return

    await msg.answer("Registratsiyadan o'tish uchun ismingizni kiriting:")
    await state.set_state(RegisterState.name)


@router.message(RegisterState.name, F.text == CANCEL_TEXT)
@router.message(RegisterState.surename, F.text == CANCEL_TEXT)
@router.message(RegisterState.age, F.text == CANCEL_TEXT)
@router.message(RegisterState.number, F.text == CANCEL_TEXT)
async def register_cancel(msg: Message, state: FSMContext):
    await state.clear()
    await msg.answer("Registratsiya bekor qilindi.", reply_markup=register_reply())


@router.message(RegisterState.name)
async def register_name(msg: Message, state: FSMContext):
    await state.update_data(name=msg.text)
    await msg.answer("Familyangizni kiriting:")
    await state.set_state(RegisterState.surename)


@router.message(RegisterState.surename)
async def register_surname(msg: Message, state: FSMContext):
    await state.update_data(surename=msg.text)
    await msg.answer("Yoshingizni kiriting:")
    await state.set_state(RegisterState.age)


@router.message(RegisterState.age)
async def register_age(msg: Message, state: FSMContext):
    if msg.text is None or not msg.text.isdigit():
        await msg.answer("Yoshni faqat raqam bilan kiriting.")
        return

    await state.update_data(age=msg.text)
    await msg.answer(
        "Telefon raqamingizni  kiriting (masalan: +998901234567):",
        reply_markup=register_phone_reply(),
    )
    await state.set_state(RegisterState.number)


@router.message(RegisterState.number)
async def register_phone(msg: Message, state: FSMContext, db):
    raw_phone = msg.text or ""

    phone = _normalize_phone(raw_phone)
    if not _is_valid_phone(phone):
        await msg.answer(
            "Telefon raqam noto'g'ri. Qo'lda qayta kiriting (masalan: +998901234567).",
            reply_markup=register_phone_reply(),
        )
        return

    await state.update_data(number=phone)

    data = await state.get_data()

    if msg.from_user:
        await db.add_user(
            msg.from_user.id,
            data["name"],
            data["surename"],
            data["age"],
            data["number"],
        )


    await msg.answer(
        text=(
            f"Ismingiz: {data['name']}\n"
            f"Familyangiz: {data['surename']}\n"
            f"Yoshingiz: {data['age']}\n"
            f"Raqamingiz: {data['number']}\n"
        ),
        reply_markup=start_reply(),
    )
    await msg.answer("Siz muvaffaqiyatli ro'yxatdan o'tdingiz!")

    await state.clear()
