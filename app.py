import asyncio
import multiprocessing
import os
import re
from datetime import datetime, timedelta
import sqlite3
import requests
from aiogram.types import CallbackQuery, ChatMember
from aiogram.utils.formatting import Text

from flask import Flask, render_template, session, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy, query

from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart

from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from _back.handlers import router
from _back.keyboards import start_menu, get_url
from _back.database.models import async_main, Counter, User
from _back.database.query import get_account_info_from_db, update_database

load_dotenv()

token = os.environ.get('BOT_TOKEN')
channel_pcc = os.environ.get('TG_PUSSYCOINCOMMUNITY_CHANNEL_ID')
bot = Bot(token=token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())

random_token = os.urandom(12).hex()
app = Flask(__name__)
app.secret_key = random_token

# Убедимся, что включаем маршрутизатор только один раз
dp.include_router(router)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
db = SQLAlchemy(app)

engine = create_engine(url='sqlite:///db.sqlite3')
Session = sessionmaker(bind=engine)
session = Session()

# from telegram.ext import Updater, CommandHandler
# def check_sub(update, context):
#     print('проверяю пописку')
#     user_id = update.message.from_user.id
#     url = f"https://api.telegram.org/bot{token}/getChatMember?chat_id={channel_pcc}&user_id={user_id}"
#     response = requests.get(url)
#     data = response.json()
#
#     if data['ok']:
#         print('подписан!')
#         status = data['result']['status']
#         if status in ['member', 'creator', 'administrator']:
#             return True
#     return False

# user_channel_status = bot.get_chat_member(chat_id=channel_pcc, user_id=user_id)
# if user_channel_status["status"] != 'left':
#     update_database(user_id)
# else:
#     print('Пользователь не подписан на канал')


# def return template(user_id):
from _back.database.query import process_tg_user_id


@app.route('/')
def index():
    user_id = request.args.get('user_id')
    balance, account_age = get_account_info_from_db(user_id)

    return render_template("index.html",
                           static_url_path='/static',
                           user_id=user_id,
                           balance=balance,
                           account_age=account_age,
                           # id_tg=id_tg,
                           # user=user,
                           #    balance=get_user_balance(user_id),
                           #    account_age=get_account_age(user_id)
                           )


# TODO кодировка user_id, если не работает secret key / проверить
# https://habr.com/ru/articles/706446/


# @app.route('/task1', methods=['POST'])
# def task_1():
#     # telegram_user_id = session.get('telegram_user_id')
#     # print(telegram_user_id)
#     pass


# @app.route('/join', methods=['POST'])
# def join():
#     url = 'https://t.me/+8K1Wfb_o_3NhNjk1'
#     # telegram_user_id = user_id
#     # print('join tui', telegram_user_id)
#     # user = User.query.filter_by(telegram_id=user_id).first()
#     telegram_user_id = request.form.get('user_id')
#     print(telegram_user_id)
#     user = session.query(User).filter_by(id_tg=telegram_user_id).first()
#     print(user)
#     # if user.var_task_main == 0:
#     #     user.var_task_main = 1
#     #     user.balance += 1000
#     #     session.commit()
#     #     session.close()
#     #     return redirect(url)
#     return redirect(url)


# @app.route('/update_user', methods=['POST'])
# def update_user_route():
#     user_id = request.form['user_id']  # предполагается, что вы передаете user_id в POST запросе
#     try:
#         update_user(user_id, var_task_main=1, balance=1000)  # обновление данных пользователя в базе данных
#         return 'Success'
#     except Exception as e:
#         return str(e)


# @app.route('/check_subscription/<int:user_id>')
# def check_subscription():
#     print("check_subscription")
#     if check_sub():  # функция проверки подписки
#
#         return jsonify({'is_subscribed': True})
#     else:
#         return jsonify({'is_subscribed': False})

# async def check_sub():
#     user_id = int(request.args.get('user_id'))
#     print('проверка подписки')
#     # bot = Bot(token='YOUR_BOT_TOKEN')
#     member = await bot.get_chat_member(chat_id=channel_pcc, user_id=user_id)
#     print(member)
#     return member.is_chat_member()


# @router.callback_query(Text(text=['subscription_check_but_pressed']))
# async def check_subs(callback: CallbackQuery, bot: Bot):
#     user_channel_status = await bot.get_chat_member(chat_id='channel_pcc', user_id=callback.from_user.id)
#
#     if user_channel_status.status != 'left':
#         await callback.answer('Спасибо за подписку!')
#     else:
#         await callback.answer('Для начала подпишись на наш канал')


# def check_sub_tg_pcc():
#     try:
#         user_id = int(request.args.get('user_id'))
#     except ValueError:
#         abort(400, "Неверно указан user_id.")  # Использование записи в журнал для ошибок также возможно
#
#     if not channel_pcc:
#         abort(500, "ID канала не настроен.")  # Использование записи в журнал для ошибок также возможно
#
#     user_channel_status = bot.get_chat_member(chat_id=channel_pcc, user_id=user_id)
#
#     # Проверка результатов вызова API, учитывая больше граничных условий
#     if user_channel_status["status"] == 'left':
#         pass
#         # Пользователь покинул канал, отправить уведомление
#         # bot.send_message(message.from_user.id, 'Вы еще не подписались!')
#     else:
#         # Здесь можно добавить логику обработки других состояний, если это необходимо
#         pass


# @app.route('/update_counter/<id_tg>', methods=['POST'])
# def update_counter(id_tg):
#     user = User.query.filter_by(id_tg=id_tg).first()
#     print('update_counter:' + user)
#     if not user:
#         return jsonify({"message": "User not found"}), 404
#     time_diff = datetime.utcnow() - user.last_updated
#     seconds_passed = time_diff.total_seconds()
#     new_count = int(seconds_passed / 72)
#     user.counter += new_count
#     user.last_updated = datetime.utcnow()
#     db.session.commit()
#     return jsonify({"counter": user.counter})
#
#
# @app.route('/get_counter/<id_tg>', methods=['GET'])
# def get_counter(id_tg):
#     user = User.query.filter_by(id_tg=id_tg).first()
#     print('get_counter:' + user)
#     if not user:
#         return jsonify({"message": "User not found"}), 404
#     return jsonify({"counter": user.counter})
#
#
# @app.route('/reset_counter/<id_tg>', methods=['POST'])
# def reset_counter(id_tg):
#     user = User.query.filter_by(id_tg=id_tg).first()
#     print('reset_counter:' + user)
#     if not user:
#         return jsonify({"message": "User not found"}), 404
#     user.counter = 0
#     user.last_updated = datetime.utcnow()
#     db.session.commit()
#     return jsonify({"message": "Counter reset"})


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
