from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from config import BOT_OWNERS
from keyboards.default.admin import BACK_TO_MAIN


BACK_MESSAGE = '👈 ORQAGA'
CONFIRM_MESSAGE = '✅ TASTIQLASH'
ALL_RIGHT_MESSAGE = '✅ XAMMASI TO\'G\'RI'
CANCEL_MSG = '🚫 BEKOR QILISH'
DEPARTAMENT = 'RAXBARIYAT'
PERSONAL = 'XODIMLAR'
ADD_PERSONAL = 'XODIMLAR QO\'SHISH'
ADMIN = "Admin Panel"
PROFIL = "Profil"


# Vazifalar 
VAZIFALARIM = "VAZIFALARIM"
VAZIFA_YUKLASH = "VAZIFALAR" # Admins
ADD_VAZIFA = "VAZIFA YUKLASH"
BERILGARN_VAZIFALAR = "BERILGAN VAZIFALAR"
YAKUNLANGAN_VAZIFALAR = "YAKUNLANGAN VAZIFALAR"
BARCHA_VAZIFALAR = "BARCHA VAZIFALAR"


# Bo'lim [Departament]
BOLIM = "BO'LIMLAR"
BOLIM_YARATISH = "Bo'lim yaratish"
BOLIM_OCHIRISH = "Bo'limni ochirish"

def cmd_start(chat_id=None):

    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add(VAZIFALARIM, PERSONAL)
    markup.add(PROFIL)

    if chat_id in BOT_OWNERS:
        markup.add(VAZIFA_YUKLASH, BOLIM)
        markup.add(ADMIN)

    return markup



def admin_cmd_start(chat_id=None):

    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    if chat_id in BOT_OWNERS:
        markup.add(VAZIFA_YUKLASH, BOLIM)
        markup.add(PROFIL, PERSONAL)
        markup.add(ADMIN)

    return markup



def add_personal():

    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add(ADD_PERSONAL)




def vazifa_yuklash_btn():

    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add(ADD_VAZIFA, BARCHA_VAZIFALAR)
    markup.add(YAKUNLANGAN_VAZIFALAR)
    markup.add(BERILGARN_VAZIFALAR)
    markup.add(BACK_TO_MAIN)

    return markup

    

def bolim_main():

    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add(BOLIM_YARATISH, BOLIM_OCHIRISH)
    markup.add(BACK_TO_MAIN)

    return markup


