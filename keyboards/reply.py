from aiogram.types import ReplyKeyboardMarkup,ReplyKeyboardRemove,KeyboardButton

def start_reply():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Mahsulotlar"),KeyboardButton(text="Mening buyurtmalarim")],
            [KeyboardButton(text="Profile")]
        ],
        resize_keyboard=True
    )

def register_reply():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Register")]
        ],
        resize_keyboard=True
    )