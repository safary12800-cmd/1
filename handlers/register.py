import re

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from keyboards.reply import cancel_reply, phone_request_reply, register_reply, start_reply
from states.register import RegisterState

router = Router()

_PHONE_PATTERN = re.compile(r"^\+?\d{9,15}$")


@router.message(F.text.in_({"Bekor qilish", "bekor qilish"}))
async def cancel_register(msg: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.clear()
    await msg.answer("Registratsiya bekor qilindi.", reply_markup=register_reply())


@router.message(F.text == "Register")
async def register_start(msg: Message, state: FSMContext, db):
    if msg.from_user and await db.is_user_exists(msg.from_user.id):
        await msg.answer(
            "Siz allaqachon registratsiyadan o'tgansiz.",
            reply_markup=start_reply(),
        )
        await state.clear()
        return

    await msg.answer(
        "Registratsiya boshlandi. Ismingizni kiriting:",
        reply_markup=cancel_reply(),
    )
    await state.set_state(RegisterState.name)


@router.message(RegisterState.name)
async def register_name(msg: Message, state: FSMContext):
    name = (msg.text or "").strip()
    if len(name) < 2:
        await msg.answer("Ism kamida 2 ta harfdan iborat bo'lsin.")
        return

    await state.update_data(name=name)
    await msg.answer("Familyangizni kiriting:")
    await state.set_state(RegisterState.surename)


@router.message(RegisterState.surename)
async def register_surename(msg: Message, state: FSMContext):
    surename = (msg.text or "").strip()
    if len(surename) < 2:
        await msg.answer("Familiya kamida 2 ta harfdan iborat bo'lsin.")
        return

    await state.update_data(surename=surename)
    await msg.answer("Yoshingizni kiriting (masalan: 24):")
    await state.set_state(RegisterState.age)


@router.message(RegisterState.age)
async def register_age(msg: Message, state: FSMContext):
    age_text = (msg.text or "").strip()
    if not age_text.isdigit():
        await msg.answer("Yosh faqat raqam bo'lishi kerak.")
        return

    age = int(age_text)
    if age < 14 or age > 100:
        await msg.answer("Yosh 14 va 100 oralig'ida bo'lishi kerak.")
        return

    await state.update_data(age=age)
    await msg.answer(
        "Telefon raqamingizni yuboring.",
        reply_markup=phone_request_reply(),
    )
    await state.set_state(RegisterState.number)


@router.message(RegisterState.number)
async def register_number(msg: Message, state: FSMContext, db):
    phone_raw = msg.contact.phone_number if msg.contact else (msg.text or "").strip()
    phone = phone_raw.replace(" ", "")

    if not _PHONE_PATTERN.fullmatch(phone):
        await msg.answer(
            "Telefon raqamingiz notogri. Masalan: +998901234567",
            reply_markup=phone_request_reply(),
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
            "Registratsiya muvaffaqiyatli yakunlandi.\n\n"
            f"Ism: {data['name']}\n"
            f"Familiya: {data['surename']}\n"
            f"Yosh: {data['age']}\n"
            f"Telefon: {data['number']}"
            "\nRol: Foydalanuvchi"
        ),
        reply_markup=start_reply(),
    )

    await state.clear()
