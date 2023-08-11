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

from bot import engine
from utility.db import Department, Personnel, Task
from keyboards.inline import start_kayboard

Session = sessionmaker(bind=engine)
session = Session()


# Personal actions goes here (bot direct messages)
# Here is some example !ping command ...
@dp.message_handler(is_owner=True, commands="ping", commands_prefix="!/")
async def cmd_ping_bot(message: types.Message):
    await message.reply("<b>👊 Up & Running!</b>\n\n")



@dp.message_handler(Command("start"))
async def start(message: types.Message):
    await message.answer("Привет! Я Task Manager Bot. Чем я могу вам помочь?", reply_markup=start_kayboard)




@dp.message_handler(commands=['create_task'])
async def create_task(message: types.Message):
    departments = session.query(Department).all()
    if not departments:
        await message.answer("Сначала создайте хотя бы один отдел.")
        return

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for department in departments:
        keyboard.add(department.name)

    await message.answer("Выберите отдел:", reply_markup=keyboard)
    await dp.register_next_step_handler(message, process_create_task)

async def process_create_task(message: types.Message):
    selected_department_name = message.text
    department = session.query(Department).filter_by(name=selected_department_name).first()
    if not department:
        await message.answer("Выбранный отдел не существует.")
        return

    await message.answer("Введите текст задачи:")
    await dp.register_next_step_handler(message, lambda msg: save_task(msg, department))

def save_task(message: types.Message, department: Department):
    task_text = message.text
    new_task = Task(text=task_text, department_id=department.id)
    session.add(new_task)
    session.commit()
    bot.send_message(message.chat.id, f"Задача '{task_text}' добавлена в отдел '{department.name}'.")


# @dp.message_handler(commands=["start"])
# async def start_command(message: types.Message):

#     await message.answer(f"User: {message.from_user.full_name}")


# @dp.message_handler(commands=['create_department'])
# async def create_department(message: types.Message):
#     await message.answer("Введите название нового отдела:")
#     await bot.register_next_step_handler(message, process_create_department)


# async def process_create_department(message: types.Message):
#     department_name = message.text
#     new_department = Department(name=department_name)
#     session.add(new_department)
#     session.commit()
#     await message.answer(f"Отдел '{department_name}' создан!")


# @dp.message_handler(commands=['create_task'])
# async def create_task(message: types.Message):
#     departments = session.query(Department).all()
#     if not departments:
#         await message.answer("Сначала создайте хотя бы один отдел.")
#         return

#     keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
#     for department in departments:
#         keyboard.add(department.name)

#     await message.answer("Выберите отдел:", reply_markup=keyboard)
#     await bot.register_next_step_handler(message, process_create_task)


# async def process_create_task(message: types.Message):
#     selected_department_name = message.text
#     department = session.query(Department).filter_by(name=selected_department_name).first()
#     if not department:
#         await message.answer("Выбранный отдел не существует.")
#         return

#     await message.answer("Введите текст задачи:")
#     await bot.register_next_step_handler(message, lambda msg: save_due_date(msg, department))


# @dp.message_handler(lambda message: message.chat.id in session and "text" in session[message.chat.id])
# async def save_due_date(message: types.Message):
#     try:
#         due_date = datetime.datetime.strptime(message.text, '%Y-%m-%d %H:%M')
#     except ValueError:
#         await message.answer("Неверный формат даты и времени. Пожалуйста, введите в формате YYYY-MM-DD HH:MM:")
#         return

#     task_data = session[message.chat.id]
#     department_id = task_data["department_id"]
#     department = session.query(Department).get(department_id)  # Получаем объект отдела по ID
#     new_task = Task(text=task_data["text"], department_id=department_id, due_date=due_date)
#     session.add(new_task)
#     session.commit()

#     del session[message.chat.id]

#     await message.answer(f"Задача '{new_task.text}' добавлена в отдел '{department.name}'. Дедлайн: {due_date}.")

#     personnel_ids = [p.user_id for p in session.query(Personnel).all()]

#     # Send the task to personnel
#     for user_id in personnel_ids:
#         try:
#             await bot.send_message(user_id, f"Новая задача в отделе '{department.name}': {new_task.text}\nДедлайн: {due_date}")
#         except exceptions.BotBlocked:
#             logging.error(f"Target [ID:{user_id}]: blocked by user")
#         except exceptions.ChatNotFound:
#             logging.error(f"Target [ID:{user_id}]: invalid user ID")
#         except exceptions.RetryAfter as e:
#             logging.error(f"Target [ID:{user_id}]: Flood limit is exceeded. Sleep {e.timeout} seconds.")
#             await asyncio.sleep(e.timeout)
#         except exceptions.UserDeactivated:
#             logging.error(f"Target [ID:{user_id}]: user is deactivated")



# @dp.message_handler(lambda message: message.chat.id in session and "text" in session[message.chat.id])
# async def save_due_date(message: types.Message):
#     try:
#         due_date = datetime.datetime.strptime(message.text, '%Y-%m-%d %H:%M')
#     except ValueError:
#         await message.answer("Неверный формат даты и времени. Пожалуйста, введите в формате YYYY-MM-DD HH:MM:")
#         return

#     task_data = session[message.chat.id]
#     department_id = task_data["department_id"]
#     department = session.query(Department).get(department_id)  # Получаем объект отдела по ID
#     new_task = Task(text=task_data["text"], department_id=department_id, due_date=due_date)
#     session.add(new_task)
#     session.commit()

#     del session[message.chat.id]

#     await message.answer(f"Задача '{new_task.text}' добавлена в отдел '{department.name}'. Дедлайн: {due_date}.")

#     personnel_ids = [p.user_id for p in session.query(Personnel).all()]

#     # Send the task to personnel
#     for user_id in personnel_ids:
#         try:
#             await bot.send_message(user_id, f"Новая задача в отделе '{department.name}': {new_task.text}\nДедлайн: {due_date}")
#         except exceptions.BotBlocked:
#             logging.error(f"Target [ID:{user_id}]: blocked by user")
#         except exceptions.ChatNotFound:
#             logging.error(f"Target [ID:{user_id}]: invalid user ID")
#         except exceptions.RetryAfter as e:
#             logging.error(f"Target [ID:{user_id}]: Flood limit is exceeded. Sleep {e.timeout} seconds.")
#             await asyncio.sleep(e.timeout)
#         except exceptions.UserDeactivated:
#             logging.error(f"Target [ID:{user_id}]: user is deactivated")


# @dp.message_handler(commands=['add_personnel'])
# async def add_personnel(message: types.Message):
#     await message.answer("Введите имя сотрудника:")
#     await bot.register_next_step_handler(message, process_add_personnel_name)


# async def process_add_personnel_name(message: types.Message):
#     name = message.text
#     await message.answer("Введите должность сотрудника:")
#     session[message.chat.id] = {"name": name}

# @dp.message_handler(lambda message: message.chat.id in session and "name" in session[message.chat.id])
# async def process_add_personnel_position(message: types.Message):
#     name = session[message.chat.id]["name"]
#     position = message.text
#     new_personnel = Personnel(user_id=message.from_user.id, name=name, position=position)
#     session.add(new_personnel)
#     session.commit()

#     del session[message.chat.id]["name"]

#     await message.answer(f"Сотрудник '{name}' добавлен в список персонала с должностью '{position}'.")

