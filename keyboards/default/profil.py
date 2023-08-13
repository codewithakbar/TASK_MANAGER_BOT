from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from config import BOT_OWNERS
from keyboards.default.admin import BACK_TO_MAIN



# YANGILASH = "MA'LUMOTLARNI YANGILASH"
NAME = "Ismni o'zgartishi"
FAMILIYA = "Fam. o'zgartishi"
PHONE = "Tel. yangilash"
LAVOZIM = "Lavoz. yangilash"


def profile_murkups():
    
    murkup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    murkup.add(NAME, FAMILIYA)
    murkup.add(PHONE, LAVOZIM)
    murkup.add(BACK_TO_MAIN)
    
    return murkup

