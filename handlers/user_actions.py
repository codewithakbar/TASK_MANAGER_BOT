import datetime
import asyncio
from aiogram import types
from dispatcher import dp, bot
from config import BOT_OWNERS


async def send_message_every_10_sec():
    await bot.send_message([984573662, 933986259], 'H3110 FRI3ND')
    while True:
        await bot.send_message(984573662, datetime.datetime.now().strftime('%d.%m.%Y'))
        await asyncio.sleep(10)

        