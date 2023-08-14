from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from config import BOT_OWNERS
from keyboards.default.admin import BACK_TO_MAIN


BACK_MESSAGE = '👈 ORQAGA'
CONFIRM_MESSAGE = '✅ TASTIQLASH'
ALL_RIGHT_MESSAGE = '✅ XAMMASI TO\'G\'RI'
CANCEL_MSG = '🚫 BEKOR QILISH'
DEPARTAMENT = 'RAXBARIYAT'
VAZIFA_YUKLASH = "VAZIFA YUKLASH"
VAZIFALARIM = "VAZIFALARIM"
PERSONAL = 'XODIMLAR'
ADD_PERSONAL = 'XODIMLAR QO\'SHISH'
BOLIM = "BO'LIM YARATISH"
ADMIN = "Admin Panel"
PROFIL = "Profil"




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
    markup.add(VAZIFA_YUKLASH)
    markup.add(BACK_TO_MAIN)

    return markup

    