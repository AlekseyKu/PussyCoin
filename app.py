import asyncio
import multiprocessing
import os

from flask import request
from flask import Flask, render_template, session

from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart

from dotenv import load_dotenv

from _back.handlers import router
from _back.keyboards import start_menu, get_url
from _back.database.models import async_main
from _back.database.query import get_account_info_from_DB


load_dotenv()


token = os.environ.get('BOT_TOKEN')
bot = Bot(token=token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())

random_token = os.urandom(12).hex()
app = Flask(__name__)
app.secret_key = random_token


# Убедимся, что включаем маршрутизатор только один раз
dp.include_router(router)
    

@app.route('/')
def index():
    user_id = request.args.get('user_id')
    balance, account_age = get_account_info_from_DB(user_id)

    return render_template("index.html", 
                           static_url_path='/static', 
                           user_id=user_id, 
                           balance = balance,
                           account_age = account_age, 
                        #    balance=get_user_balance(user_id),
                        #    account_age=get_account_age(user_id)
    )

# TODO кодировка user_id, если не работает secret key / проверить
# https://habr.com/ru/articles/706446/

def run_flask():
    app.run(ssl_context=(
        'D:\\_py_projects\\PussyCoin\\cert\\localhost.crt', 'D:\\_py_projects\\PussyCoin\\cert\\localhost.key'),
        host='0.0.0.0', port=443)


async def main():
    await async_main()
    await bot.set_my_commands(commands=start_menu)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        flask_process = multiprocessing.Process(target=run_flask).start()
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')







