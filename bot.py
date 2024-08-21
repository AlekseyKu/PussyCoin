import asyncio
import os

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from dotenv import load_dotenv

from _back.handlers import router
from _back.keyboards import start_menu
from _back.database.models import async_main

load_dotenv()

token = os.environ.get('TOKEN')
bot = Bot(token=token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

# Убедимся, что включаем маршрутизатор только один раз
dp.include_router(router)



# async def get_user_avatar(user_id: int, bot: Bot) -> str:
#     try:
#         # Получаем фотографии профиля пользователя
#         photos = await bot.get_user_profile_photos(user_id)
#         if photos.total_count > 0:
#             # Используем первую фотографию
#             file_id = photos.photos[0][0].file_id
#             file = await bot.get_file(file_id)
#             # Создаем полный URL к фотографии
#             avatar_url = f"https://api.telegram.org/file/bot{bot.token}/{file.file_path}"
#             return avatar_url
#     except Exception as e:
#         print(f"Error fetching avatar: {e}")
#     return "default-avatar.png"  # Путь к дефолтной иконке


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
