from aiogram.types import ReplyKeyboardMarkup, KeyboardButton



BACK_MESSAGE = '👈 ORQAGA'
CONFIRM_MESSAGE = '✅ TASTIQLASH'
ALL_RIGHT_MESSAGE = '✅ XAMMASI TO\'G\'RI'
CANCEL_MSG = '🚫 BEKOR QILISH'
DEPARTAMENT = 'RAXBARIYAT'
PERSONAL = 'XODIMLAR'
ADD_PERSONAL = 'XODIMLAR QO\'SHISH'
BOLIM = "BO'LIM YARATISH"


def cmd_start():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add(DEPARTAMENT, PERSONAL)
    markup.add(BOLIM)

    return markup


