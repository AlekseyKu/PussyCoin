import asyncio
import os

from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from dotenv import load_dotenv

from _back.handlers import router
from _back.keyboards import start_menu, get_url
from _back.database.models import async_main, Counter, User

load_dotenv()

token = os.environ.get('BOT_TOKEN')
bot = Bot(token=token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

# Убедимся, что включаем маршрутизатор только один раз
dp.include_router(router)


async def main():
    await async_main()
    await bot.set_my_commands(commands=start_menu)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
