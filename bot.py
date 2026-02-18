import asyncio

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config import config
from database.database import Database
from handlers.register import router as register_router
from handlers.profile import router as profile_router
from handlers.start import router as start_router


async def main():
    if not config.BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN .env ichida topilmadi")

    bot = Bot(token=config.BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    db = Database()
    await db.connect()
    dp["db"] = db

    dp.include_router(start_router)
    dp.include_router(register_router)
    dp.include_router(profile_router)

    try:
        await dp.start_polling(bot)
    finally:
        await db.close()
        await bot.session.close()


if __name__ == "__main__":
    print("Bot ishga tushmoqda...")
    asyncio.run(main())
