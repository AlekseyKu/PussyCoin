import asyncio
from aiogram import types, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage

from flask import session, current_app

from _back.keyboards import get_url
import _back.database.requests as rq

from _back.database.query import process_tg_user_id


router = Router()
storage = MemoryStorage()

from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from _back.database.models import User


# DATABASE_URL = 'sqlite:///db.sqlite3'
# engine = create_engine(DATABASE_URL)
# Session = sessionmaker(bind=engine)

@router.message(CommandStart())
async def start(message: types.Message):
    await rq.set_user(message.from_user.id, message.from_user.first_name, message.from_user.last_name)
    tg_user_id = message.from_user.id
    print(tg_user_id)
    print('информация по пользователю внесена')

    start_text = (f'🔥 Hello, {message.from_user.first_name}! '
                  f'Collect PussyCoin and join community.')

    print('bot started')

    play_kb = get_url(message.from_user.id)

    # await process_tg_user_id(tg_user_id)

    await message.answer(text=start_text, reply_markup=play_kb)
