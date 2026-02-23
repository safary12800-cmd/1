from aiogram import F, Router
from aiogram.types import Message

from filtr.filtr import RoleFilter
from keyboards.inline import products_inline

router = Router()


@router.message(lambda msg: msg.text == "Yonalishlar")
async def show_products(message: Message, db):
    products = await db.get_products()
    await message.answer(
        "🛍 Yonalishlar:",
        reply_markup=products_inline(products),
    )


@router.message(
    F.text.in_({"Yonalishlar(Admin)", "📋 Yonalishlar(Admin)"}),
    RoleFilter("admin"),
)
async def show_products_admin(message: Message, db):
    products = await db.get_products()
    await message.answer(
        "🛍 Yonalishlar:",
        reply_markup=products_inline(products),
    )
