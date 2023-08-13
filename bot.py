from sqlalchemy import create_engine
import handlers


import asyncio
from aiogram import executor
from dispatcher import dp
from utility.db import Base
from sqlalchemy.orm import sessionmaker


DATABASE_URL = 'sqlite:///task_manager.db'
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()


if __name__ == "__main__":
    Base.metadata.create_all(engine)
    executor.start_polling(dp, skip_updates=True)
