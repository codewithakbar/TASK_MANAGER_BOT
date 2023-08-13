from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


ADD_PERSONAL = "XODIM QOSHISH"
DELETE_PERSONAL = "XODIMNI OCHIRISH"
USERS = "FOYDALANUVCHILAR"
BACK_TO_MAIN = "ORQAGA"

def add_personal():
    
    murkup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    murkup.add(ADD_PERSONAL, DELETE_PERSONAL)
    murkup.add(USERS)
    murkup.add(BACK_TO_MAIN)

    return murkup


def back_to_main():
    murkup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    murkup.add(BACK_TO_MAIN)

    return murkup

    

