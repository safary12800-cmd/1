from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def start_reply():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="Mahsulotlar"),
                KeyboardButton(text="Mening buyurtmalarim"),
            ],
            [KeyboardButton(text="Profile")],
        ],
        resize_keyboard=True,
    )


def register_reply():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Register")]],
        resize_keyboard=True,
    )


def register_phone_reply():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Bekor qilish")],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )
