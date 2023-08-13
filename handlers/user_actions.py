import datetime
import asyncio
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from bot import Session
from dispatcher import dp, bot
from config import BOT_OWNERS
from keyboards.default.commands import cmd_start

from keyboards.default.profil import NAME, FAMILIYA, PHONE, LAVOZIM
from utility.db import User


# FSM states
class UserDataForm(StatesGroup):
    waiting_for_first_name = State()
    waiting_for_last_name = State()
    waiting_for_phone = State()
    waiting_for_lavozim = State()


        
@dp.message_handler(text=f"{NAME}")
async def change_user_first_name(message: types.Message):
    await message.answer("<b>Iltimos Ismingizni kiriting:</b>")
    await UserDataForm.waiting_for_first_name.set()


@dp.message_handler(text=f"{FAMILIYA}")
async def change_user_last_name(message: types.Message):
    await message.answer("<b>Iltimos Familiyangizni kiriting:</b>")
    await UserDataForm.waiting_for_last_name.set()


@dp.message_handler(text=f"{PHONE}")
async def change_user_phone(message: types.Message):
    await message.answer("<b>Iltimos Telefon raqamingizni kiriting:</b>")
    await UserDataForm.waiting_for_phone.set()


@dp.message_handler(text=f"{LAVOZIM}")
async def change_user_lavozim(message: types.Message):
    await message.answer("<b>Iltimos Lavozimingizni kiriting:</b>")
    await UserDataForm.waiting_for_lavozim.set()



@dp.message_handler(state=UserDataForm.waiting_for_first_name)
async def update_first_name(message: types.Message, state: FSMContext):
    new_first_name = message.text
    username = message.from_user.username
    msg_chat_id = message.chat.id

    session = Session()
    user = session.query(User).filter_by(chat_id=message.chat.id).first()
    if user:
        user.first_name = new_first_name
        session.commit()
        await message.answer("Ismingiz Yangiliandi", reply_markup=cmd_start(msg_chat_id))
    else:
        await message.answer("Fo'ydalanuvchi to'pilmdi.", reply_markup=cmd_start(msg_chat_id))
    
    await state.finish()


@dp.message_handler(state=UserDataForm.waiting_for_last_name)
async def update_last_name(message: types.Message, state: FSMContext):
    new_last_name = message.text
    username = message.from_user.username
    msg_chat_id = message.chat.id

    session = Session()
    user = session.query(User).filter_by(chat_id=message.chat.id).first()
    if user:
        user.last_name = new_last_name
        session.commit()
        await message.answer("Familiyangiz yangilandi!", reply_markup=cmd_start(msg_chat_id))
    else:
        await message.answer("Fo'ydalanuvchi to'pilmdi.", reply_markup=cmd_start(msg_chat_id))
    
    await state.finish()


@dp.message_handler(state=UserDataForm.waiting_for_phone)
async def update_phone(message: types.Message, state: FSMContext):
    new_phone_number = message.text
    username = message.from_user.username
    msg_chat_id = message.chat.id

    session = Session()
    user = session.query(User).filter_by(chat_id=message.chat.id).first()
    if user:
        user.phone = new_phone_number
        session.commit()
        await message.answer("Telefon raqmingiz yangilandi!", reply_markup=cmd_start(msg_chat_id))
    else:
        await message.answer("Fo'ydalanuvchi to'pilmdi.", reply_markup=cmd_start(msg_chat_id))
    
    await state.finish()



@dp.message_handler(state=UserDataForm.waiting_for_lavozim)
async def update_phone(message: types.Message, state: FSMContext):
    new_lavozim = message.text
    username = message.from_user.username
    msg_chat_id = message.chat.id

    session = Session()
    user = session.query(User).filter_by(chat_id=message.chat.id).first()
    if user:
        user.lavozim = new_lavozim
        session.commit()
        await message.answer("Lavozimingiz yangilandi!", reply_markup=cmd_start(msg_chat_id))
    else:
        await message.answer("Fo'ydalanuvchi to'pilmdi.", reply_markup=cmd_start(msg_chat_id))
    
    await state.finish()