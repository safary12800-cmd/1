from aiogram import Router,F
from aiogram.types import Message
from states.register import RegisterState
from aiogram.fsm.context import FSMContext


router=Router()

@router.message(F.text=="Register")
async def register_start(msg:Message,state:FSMContext):
    await msg.answer("Registratsiyadan o'tish uchun ismingizni kiriting: ")
    await state.set_state(RegisterState.name)

@router.message(RegisterState.name)
async def register_name(msg:Message,state:FSMContext):
    await state.update_data(name=msg.text)
    await msg.answer("Familyangizni kiriting: ")
    await state.set_state(RegisterState.surename)

@router.message(RegisterState.surename)
async def register_surename(msg:Message,state:FSMContext):
    await state.update_data(surename=msg.text)
    await msg.answer("Yoshingizni kiriting: ")
    await state.set_state(RegisterState.age)

@router.message(RegisterState.age)
async def register_age(msg:Message,state:FSMContext):
    await state.update_data(age=msg.text)
    await msg.answer("Raqamingizni  kiriting: ")
    await state.set_state(RegisterState.number)

@router.message(RegisterState.number)
async def register_number(msg:Message,state:FSMContext,db):
    await state.update_data(number=msg.text)
    
    data=await state.get_data()
    await msg.answer(
        text=(
            f"Ismingiz: {data['name']}\n"
            f"Familyangiz: {data['surename']}\n"
            f"Yoshingiz: {data['age']}\n"
            f"Raqamingiz: {data['number']}\n"
        )
    )
    if msg.from_user:
        await db.add_user(msg.from_user.id,data["name"],data["surename"],data["age"],data["number"])

    await state.clear()
