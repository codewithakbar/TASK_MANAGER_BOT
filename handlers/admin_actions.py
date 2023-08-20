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
from keyboards.default.commands import ADD_VAZIFA, ADMIN, BOLIM, BOLIM_YARATISH, VAZIFA_YUKLASH, bolim_main, vazifa_yuklash_btn
from keyboards.default.admin import ADD_PERSONAL, USERS, DELETE_PERSONAL, USERS_DELETE, back_to_main

delete_user_callback = CallbackData("delete_user", "user_id")



class PersonalDataForm(StatesGroup):
    waiting_for_username = State()
    waiting_for_first_name = State()
    waiting_for_last_name = State()


class DepartamentDataForm(StatesGroup):
    waiting_for_name = State()



class TaskAssignmentStates(StatesGroup):
    waiting_for_task_details = State()




@dp.message_handler(is_owner=True, text=f"{ADMIN}")
async def admin_panel(message: types.Message):
    await message.reply("<b>Admin Panel!</b>\n\n", reply_markup=add_personal())



@dp.message_handler(is_owner=True, text=f"{VAZIFA_YUKLASH}")
async def vazifa_yuklash(message: types.Message):
    await message.reply("<b>Vazifalar bo'limi!</b>\n\n", reply_markup=vazifa_yuklash_btn())



@dp.message_handler(is_owner=True, text=f"{ADD_VAZIFA}")
async def vazifa_yuklash(message: types.Message):
    session = Session()
    users = session.query(Personal).all()

    if not users:
        await message.answer("Xodimlar topilmadi.")
        return

    keyboard = types.InlineKeyboardMarkup()

    for user in users:
        button_text = f"{user.first_name} {user.last_name}"
        callback_data = f"for_task:{user.id}"
        keyboard.add(types.InlineKeyboardButton(text=button_text, callback_data=callback_data))

    await message.reply("<b>Vazifa yuklash uchun xodimlardan birini tanlang:</b>\n\n", reply_markup=keyboard)



@dp.callback_query_handler(lambda c: c.data.startswith("for_task:"), state=None)
async def assign_task_callback(callback_query: types.CallbackQuery, state: FSMContext):
    user_id = int(callback_query.data.split(":")[1])
    # Load the user from the database based on user_id
    session = Session()
    user = session.query(Personal).get(user_id)
    if user:
        await callback_query.message.answer(f"Siz {user.first_name} {user.last_name} ni tanladingiz.")
        await callback_query.message.answer("Iltimos, vazifa ma'lumotlarini kiriting:")
        
        # Set the state to waiting_for_task_details
        await TaskAssignmentStates.waiting_for_task_details.set()

        # Store the user_id in the state for later use
        async with state.proxy() as data:
            data['user_id'] = user_id

    else:
        await callback_query.message.answer("Foydalanuvchi topilmadi.")
    session.close()

@dp.message_handler(state=TaskAssignmentStates.waiting_for_task_details)
async def process_task_details(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        user_id = data['user_id']
    session = Session()
    user = session.query(Personal).get(user_id)
    
    task_details = message.text

    # Create a Task instance and add it to the session
    new_task = Task(text=task_details)  # Replace with appropriate department_id
    session.add(new_task)
    session.commit()
    
    # keyboard = types.InlineKeyboardMarkup()

    
    callback_data = f"for_task:{user.id}"
    keyboard = types.InlineKeyboardMarkup(
        inline_keyboard=[[
            types.InlineKeyboardButton(text="✅ Tasdiqlash", callback_data="confirm_a"),
            types.InlineKeyboardButton(text="❌ Bekor qilish", callback_data="cancel_a"),
        ]]
    )

    await bot.send_message(user.chat_id, f"Yangi vazifa taqdim etildi:\n\n{task_details}", reply_markup=keyboard)
    
    await message.answer("Vazifa muvaffaqiyatli taqdim etildi!")
    
    # Finish the conversation by resetting the state
    await state.finish()
    

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
async def add_personal_in_admin(message: types.Message):
    session = Session()
    users = session.query(User).all()

    if not users:
        await message.answer("There are no users registered.")
        return

    keyboard = types.InlineKeyboardMarkup()

    for user in users:
        button_text = f"{user.first_name} {user.last_name}"
        callback_data = f"add_personal:{user.id}"
        keyboard.add(types.InlineKeyboardButton(text=button_text, callback_data=callback_data))


    await message.answer("Xodim qoshish uchun ism ustiga bo'sing:", reply_markup=keyboard)



@dp.callback_query_handler(lambda c: c.data.startswith("add_personal:"))
async def add_personal_callback(callback_query: types.CallbackQuery):
    user_id = int(callback_query.data.split(":")[1])

    session = Session()
    user = session.query(User).get(user_id)
    personal = session.query(Personal).get(user_id)

    if user:
        if personal:
            await callback_query.answer("Qoshilgassn!!!")
        else:

            new_personal = Personal(
                user_id=user.id,
                first_name=user.first_name,
                last_name=user.last_name,
                chat_id=user.chat_id,
            )
            session.add(new_personal)
            session.commit()

            await callback_query.answer("User added to personal_user model")
    else:
        await callback_query.answer("Qoshilgan!!!")







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



