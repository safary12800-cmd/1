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
            [KeyboardButton(text="Raqamni yuborish", request_contact=True)],
            [KeyboardButton(text="Bekor qilish")],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def kataloglar_reply():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Telefonlar"), KeyboardButton(text="Frontend")],
            [KeyboardButton(text="Backend"), KeyboardButton(text="Dizayn")],
        ],
        resize_keyboard=True,
    )
