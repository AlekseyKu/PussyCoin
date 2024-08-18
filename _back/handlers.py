from aiogram import types, Router
from aiogram.filters import CommandStart
from aiogram.fsm.storage.memory import MemoryStorage

from _back.keyboards import get_url
import _back.database.requests as rq

router = Router()
storage = MemoryStorage()


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


    await message.answer(text=start_text, reply_markup=play_kb)
