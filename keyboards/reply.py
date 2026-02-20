from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def start_reply() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Mahsulotlar"), KeyboardButton(text="Mening buyurtmalarim")],
            [KeyboardButton(text="Profile")],
        ],
        resize_keyboard=True,
    )


def register_reply() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Register")]],
        resize_keyboard=True,
    )


def cancel_reply() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Bekor qilish")]],
        resize_keyboard=True,
    )


def phone_request_reply() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Telefon raqamni yuborish", request_contact=True)],
            [KeyboardButton(text="Bekor qilish")],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )
def start_admin():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Register")]
            ],
        resize_keyboard=True,
    )

def start_reply_admin():

    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Register")],
            [KeyboardButton(text="Mahsulotlar"),KeyboardButton(text="Mening buyurtmalarim")],
            [KeyboardButton(text="Profile"),KeyboardButton(text="Admin panel")]
        ],
        resize_keyboard=True
    )



def admin_panel_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="➕ Mahsulot qo‘shish")],
            [KeyboardButton(text="➕ Mahsulot qo‘shish")],
            [KeyboardButton(text="📋 Mahsulotlar(Admin)")],
            [KeyboardButton(text="👥 Userlar")],
            [KeyboardButton(text="⬅️ Orqaga")]
        ],
        resize_keyboard=True
    )