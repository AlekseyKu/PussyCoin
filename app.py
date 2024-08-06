import asyncio
import multiprocessing
import os
from datetime import datetime, timedelta
import sqlite3

from flask import Flask, render_template, session, request, jsonify
from flask_sqlalchemy import SQLAlchemy

from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart

from dotenv import load_dotenv
from sqlalchemy import create_engine, literal_column
from sqlalchemy.orm import sessionmaker

from _back.handlers import router
from _back.keyboards import start_menu, get_url
from _back.database.models import async_main, Counter, User
from _back.database.query import get_account_info_from_db

load_dotenv()

token = os.environ.get('BOT_TOKEN')
bot = Bot(token=token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())

random_token = os.urandom(12).hex()
app = Flask(__name__)
app.secret_key = random_token

# Убедимся, что включаем маршрутизатор только один раз
dp.include_router(router)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
db = SQLAlchemy(app)

DATABASE_URL = 'sqlite:///db.sqlite3'

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)


@app.route('/')
def index():
    user_id = request.args.get('user_id')
    balance, account_age = get_account_info_from_db(user_id)
    # session = Session()
    # user = session.query(User).filter_by(id_tg=user_id).first()
    # if user.var_main_task == 0:
    #     print(user.var_main_task)
    #     user.balance += 1000
    #     user_update = user.var_main_task
    #     user.var_main_task = 1
    #     session.commit()
    #     session.close()
    #     return user_update
    # session.close()

    # curr_usr = db.session.query("current_user")
    # for usr in curr_usr:
    #     user = usr[0]
    #     print('usr:', user)

    # session = Session()
    # user = session.query(literal_column("current_user"))
    # user_id_tg = user.first()
    # print(user_id_tg)
    # session.close()

    return render_template("index.html",
                           static_url_path='/static',
                           user_id=user_id,
                           balance=balance,
                           account_age=account_age,
                           # user=user.var_main_task
                           # user=user_update
                           #    balance=get_user_balance(user_id),
                           #    account_age=get_account_age(user_id)
                           )


# TODO кодировка user_id, если не работает secret key / проверить
# https://habr.com/ru/articles/706446/

# @app.route('/getVarMainTask', methods=['GET'])
# def get_var_main_task():
#     session = Session()
#     user = session.query(User).first()  # Предположим, что в таблице только одна запись
#     var_main_task_value = user.var_main_task if user else 0
#     session.close()
#     return jsonify({'var_main_task': var_main_task_value})
#
#
# @app.route('/updateVarMainTask', methods=['POST'])
# def update_var_main_task():
#     data = request.get_json()
#     var_main_task_value = data.get('var_main_task')
#
#     # Обновление значения var_main_task в базе данных
#     session = Session()
#     user = session.query(User).first()  # Предположим, что в таблице только одна запись
#     if user:
#         user.var_main_task = var_main_task_value
#         session.commit()
#
#     session.close()

    # return jsonify({'status': 'success'})


@app.route('/update_button', methods=['POST'])
def update_button():
    user_id = request.args.get('user_id')
    session = Session()
    user = session.query(User).filter_by(id_tg=user_id).first()
    if user.var_main_task == 0:
        print(user.var_main_task)
        user.balance += 1000
        user_update = user.var_main_task
        user.var_main_task = 1
        session.commit()
        session.close()
        return user_update
    session.close()


@app.route('/update_counter/<id_tg>', methods=['POST'])
def update_counter(id_tg):
    user = User.query.filter_by(id_tg=id_tg).first()
    print('update_counter:' + user)
    if not user:
        return jsonify({"message": "User not found"}), 404
    time_diff = datetime.utcnow() - user.last_updated
    seconds_passed = time_diff.total_seconds()
    new_count = int(seconds_passed / 72)
    user.counter += new_count
    user.last_updated = datetime.utcnow()
    db.session.commit()
    return jsonify({"counter": user.counter})


@app.route('/get_counter/<id_tg>', methods=['GET'])
def get_counter(id_tg):
    user = User.query.filter_by(id_tg=id_tg).first()
    print('get_counter:' + user)
    if not user:
        return jsonify({"message": "User not found"}), 404
    return jsonify({"counter": user.counter})


@app.route('/reset_counter/<id_tg>', methods=['POST'])
def reset_counter(id_tg):
    user = User.query.filter_by(id_tg=id_tg).first()
    print('reset_counter:' + user)
    if not user:
        return jsonify({"message": "User not found"}), 404
    user.counter = 0
    user.last_updated = datetime.utcnow()
    db.session.commit()
    return jsonify({"message": "Counter reset"})


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
