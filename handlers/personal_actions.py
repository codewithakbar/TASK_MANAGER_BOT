import asyncio
from asyncio import exceptions
import datetime
import io
import json
import logging

from PIL import Image, ImageDraw
import requests
from io import BytesIO

from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.utils.markdown import hbold, hunderline, hpre, hlink, text
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from aiogram.dispatcher.filters.state import State, StatesGroup


from dispatcher import dp, bot
from data.config import ADMINS, CHANNELS

from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound


from bot import Session, engine
from keyboards.default.admin import BACK_TO_MAIN, add_personal, back_to_main
from keyboards.default.profil import profile_murkups
from utility.db import Department, Personal, Task, User
from keyboards.default import cmd_start, admin_cmd_start
from keyboards.default.commands import PERSONAL, PROFIL

from config import BOT_OWNERS




@dp.message_handler(text=f"{PROFIL}")
async def user_profile(message: types.Message):
    session = Session()
    user = session.query(User).filter_by(chat_id=message.chat.id).first()

    if user:
        bio = "Topilmadi" if user.bio is None else user.bio
        phone = "Topilmadi" if user.phone is None else user.phone
        lavozim = "Topilmadi" if user.lavozim is None else user.lavozim
        chat_id = "Topilmadi" if user.chat_id is None else user.chat_id
        response = f"Profil:\nIsmi: {user.first_name}\nFamiliya: {user.last_name}\nFoydalanuvchi xaqida: {bio}\nTelefon raqam: {phone}\nLavozim: {lavozim}\nChat ID: {chat_id}"

        await message.answer(response, reply_markup=profile_murkups())
    else:
        await message.answer("Nimadir xato ketti!")







# Personal actions goes here (bot direct messages)
# Here is some example !ping command ...
@dp.message_handler(is_owner=True, commands="ping", commands_prefix="!/")
async def cmd_ping_bot(message: types.Message):
    await message.reply("<b>👊 Up & Running!</b>\n\n")


@dp.message_handler(text=f"{PERSONAL}")
async def xodimlar(message: types.Message):
    session = Session()
    users = session.query(User).all()
    msg_chat_id = message.chat.id

    if not users:
        await message.answer("Xodimlar Topilmadi", reply_markup=add_personal())
        return
    
    keyboard = types.InlineKeyboardMarkup()

    for user in users:
        button_text = f"{user.first_name} {user.last_name}"
        callback_data = f"add_personal:{user.id}"
        keyboard.add(types.InlineKeyboardButton(text=button_text, callback_data=callback_data))
    
    if message.chat.id in BOT_OWNERS:
        await message.reply("Botdagi fo'ydalanuvchidal: \n\n", reply_markup=back_to_main())
        await message.answer("Xodimlar safiga qoshish uchun Ism ustiga bo'sing", reply_markup=keyboard)
    else:
        await message.reply("Xodimlar: \n\n", reply_markup=keyboard)


@dp.callback_query_handler(lambda query: query.data.startswith("add_personal:"))
async def add_personal_user(callback_query: types.CallbackQuery):
    user_id = int(callback_query.data.split(":")[1])
    
    session = Session()

    user = session.query(User).get(user_id)
    
    if user:
        await callback_query.answer("Qoshilgan!!!")
    else:
        new_personal = Personal(
            user_id=user.id,
            user_chat_id=user.chat_id
        )
        session.add(new_personal)
        session.commit()

        await callback_query.answer("User added to personal_user model")




@dp.message_handler(Command("start"))
@dp.message_handler(text=f"{BACK_TO_MAIN}")
async def start(message: types.Message):
    first_name = "" if message.from_user.first_name is None else message.from_user.first_name
    last_name = "" if message.from_user.last_name is None else message.from_user.last_name
    username = "" if message.from_user.username is None else message.from_user.username

    session = Session()

    user = session.query(User).filter_by(chat_id=message.chat.id).first()
    msg_chat_id = message.chat.id

    if user:
        await message.answer("Asosiy Menyu")
    else:
        new_user = User(username=username,
                        first_name=first_name,
                        last_name=last_name,
                        chat_id=msg_chat_id)

        session.add(new_user)
        session.commit()

    if msg_chat_id in BOT_OWNERS:
        await message.answer("Admin xush kelibsiz!", reply_markup=admin_cmd_start(msg_chat_id))
    else:
        await message.answer("Botga xush kelibsiz!", reply_markup=cmd_start(msg_chat_id))

    member = await message.bot.get_chat_member(message.chat.id, message.from_user.id)

    role = "Raxbar" if member.user.id in BOT_OWNERS else "Foydalanuvchi"
    if msg_chat_id in BOT_OWNERS:
        await message.answer(f"<b>Task Manager Bot:</b> \n<b>Foydalanuvchi:</b> <i>{user.first_name} {user.last_name}</i>\n<b>Roli</b>: <i>{role}</i>", reply_markup=admin_cmd_start(msg_chat_id))
    else:
        await message.answer(f"<b>Task Manager Bot:</b> \n<b>Foydalanuvchi:</b> <i>{user.first_name} {user.last_name}</i>\n<b>Roli</b>: <i>{role}</i>", reply_markup=cmd_start(msg_chat_id))





