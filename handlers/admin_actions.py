from aiogram import types
from aiogram.utils import callback_data
from aiogram.utils.callback_data import CallbackData

from aiogram.dispatcher.filters import Text
from aiogram.utils.markdown import hbold, hunderline, hpre, hlink, text
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from aiogram.dispatcher.filters.state import State, StatesGroup


from dispatcher import dp, bot


from bot import Session, engine

from utility.db import Department, Personal, Task, User
from keyboards.default import cmd_start, add_personal

from config import BOT_OWNERS
from keyboards.default.commands import ADMIN, BOLIM, BOLIM_YARATISH, VAZIFA_YUKLASH, bolim_main, vazifa_yuklash_btn
from keyboards.default.admin import ADD_PERSONAL, USERS, DELETE_PERSONAL, USERS_DELETE, back_to_main

delete_user_callback = CallbackData("delete_user", "user_id")



class PersonalDataForm(StatesGroup):
    waiting_for_username = State()
    waiting_for_first_name = State()
    waiting_for_last_name = State()


class DepartamentDataForm(StatesGroup):
    waiting_for_name = State()


@dp.message_handler(is_owner=True, text=f"{ADMIN}")
async def admin_panel(message: types.Message):
    await message.reply("<b>Admin Panel!</b>\n\n", reply_markup=add_personal())



@dp.message_handler(is_owner=True, text=f"{VAZIFA_YUKLASH}")
async def vazifa_yuklash(message: types.Message):
    await message.reply("<b>Vazifa Yuklash!</b>\n\n", reply_markup=vazifa_yuklash_btn())



"""             XODIMLARNI OCHIRISH                 """


@dp.message_handler(is_owner=True, text=f"{DELETE_PERSONAL}")
async def get_all_users_and_delete(message: types.Message):
    session = Session()
    users = session.query(Personal).all()

    if not users:
        await message.answer("There are no users registered.")
        return

    keyboard = types.InlineKeyboardMarkup()

    for user in users:
        button_text = f"{user.first_name} {user.last_name}"
        keyboard.add(types.InlineKeyboardButton(text=button_text, callback_data=delete_user_callback.new(user_id=user.id)))

    await message.answer("Xodimlarni birini o'chirish uchun xodim ismiga bo'sing!:", reply_markup=keyboard)


@dp.message_handler(is_owner=True, text=f"{USERS_DELETE}")
async def get_all_users_and_delete_p(message: types.Message):
    session = Session()
    users = session.query(User).all()

    if not users:
        await message.answer("There are no users registered.")
        return

    keyboard = types.InlineKeyboardMarkup()

    for user in users:
        button_text = f"{user.first_name} {user.last_name}"
        keyboard.add(types.InlineKeyboardButton(text=button_text, callback_data=delete_user_callback.new(user_id=user.id)))

    await message.answer("Foydalanuvchilardan birini o'chirish uchun xodim ismiga bo'sing!:", reply_markup=keyboard)



@dp.callback_query_handler(delete_user_callback.filter())
async def delete_user_callback_handler(query: types.CallbackQuery, callback_data: dict):
    user_id = int(callback_data["user_id"])

    session = Session()
    user = session.query(User).get(user_id)
    personal_user = session.query(Personal).get(user_id)

    if user:
        session.delete(user)
        session.commit()
        await query.answer("Foydalanuvchi muofaqiyatli ochirildi!")
    else:
        await query.answer("Foydalanuvchi topilmadi.")


    if personal_user:
        session.delete(personal_user)
        session.commit()
        await query.answer("Xodim muofaqiyatli ochirildi!")
    else:
        await query.answer("Xodim to'pilmadi.")

    await query.message.edit_reply_markup()




"""                 FOYDALANUVCHILAR                """

@dp.message_handler(is_owner=True, text=f"{USERS}")
async def get_all_users(message: types.Message):
    session = Session()
    users = session.query(User).all()

    if not users:
        await message.answer("There are no users registered.")
        return

    keyboard = types.InlineKeyboardMarkup()

    for user in users:
        button_text = f"{user.first_name} {user.last_name}"
        keyboard.add(types.InlineKeyboardButton(text=button_text, callback_data=f"view_user:{user.id}"))

    await message.answer("Select a user to view:", reply_markup=keyboard)






"""             Xodimlar qoshish Funksiyasi            """

@dp.message_handler(is_owner=True, text=f"{ADD_PERSONAL}")
async def add_personal_step1(message: types.Message):
    await message.answer("Iltimos, xodim nomini kiriting (yoki to'xtatish uchun /cancel ni bo'sing):")
    await PersonalDataForm.waiting_for_username.set()


@dp.message_handler(state=PersonalDataForm.waiting_for_username)
async def process_username(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['username'] = message.text
    await message.answer("Ismini kiriting (yoki to'xtatish uchun /cancel ni bo'sing):")
    await PersonalDataForm.next()


@dp.message_handler(lambda message: message.text.lower() == '/cancel', state=PersonalDataForm)
async def cancel_add_personal(message: types.Message, state: FSMContext):
    await message.answer("Xodim ma'lumotlarni qo'shish bekor qilindi.")
    await state.finish()


@dp.message_handler(state=PersonalDataForm.waiting_for_first_name)
async def process_first_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['first_name'] = message.text
    await message.answer("Familiyasini kiriting (yoki to'xtatish uchun /cancel ni bo'sing.):")
    await PersonalDataForm.next()


@dp.message_handler(state=PersonalDataForm.waiting_for_last_name)
async def process_last_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['last_name'] = message.text


    await message.answer("Xodim ma'lumotlari muvaffaqiyatli qo'shildi")
    await state.finish()





# Bo'limlar 

@dp.message_handler(is_owner=True, text=f"{BOLIM}")
async def bolim_asosiy(message: types.Message):

    session = Session()
    users = session.query(Department).all()

    if not users:
        await message.answer("There are no Departament registered.")
        return

    keyboard = types.InlineKeyboardMarkup()

    for user in users:
        button_text = f"{user.name}"
        keyboard.add(types.InlineKeyboardButton(text=button_text, callback_data=f"view_user:{user.id}"))


    await message.answer("Barcha Bo'limlar...", reply_markup=keyboard)
    await message.answer("ok...", reply_markup=bolim_main())



@dp.message_handler(is_owner=True, text=f"{BOLIM_YARATISH}")
async def add_bolim_asosiy_step1(message: types.Message):
    await message.answer("Iltimos, Bo'lim nomini kiriting (yoki to'xtatish uchun /cancel ni bo'sing):")
    await DepartamentDataForm.waiting_for_name.set()



@dp.message_handler(state=DepartamentDataForm.waiting_for_name)
async def add_bolim_asosiy_step2(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['department_name'] = message.text
    

    department_name = data['department_name']
    
    new_department = Department(name=department_name)

    session = Session()
    session.add(new_department)
    session.commit()

    await state.finish()
    await message.answer(f"Bo'lim '{department_name}' muvaffaqiyatli yaratildi!", reply_markup=back_to_main())



