import os
import requests
import asyncio
import threading
from datetime import datetime

from flask import Flask, render_template, session, request, jsonify, url_for
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.future import select

from _back.database.query import get_account_info_from_db
from _back.database.models import User, async_session

random_token = os.urandom(12).hex()
app = Flask(__name__)
app.secret_key = random_token

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
db = SQLAlchemy(app)


# DATABASE_URL = 'sqlite:///db.sqlite3'
# engine = create_engine(DATABASE_URL)
# Session = sessionmaker(bind=engine)


@app.route('/')
async def index():
    user_id = request.args.get('user_id')

    # Проверяем значение var_main_task перед выполнением других операций
    async with async_session() as session:
        # Находим пользователя по user_id
        result = await session.execute(select(User).where(User.id_tg == user_id))
        user = result.scalar_one_or_none()

        if user:
            asyncio.create_task(mining_pussies(user, session))

            # balance, account_age = await get_account_info_from_db(user_id)
            var_main_task = user.var_main_task
            balance = user.balance
            account_age = user.account_age
            id_refer = user.id_refer
            mine_friends = user.mine_friends
            mine_pussies = user.mine_pussies
            count_friends = user.count_friends
            activity_counter = user.activity_counter

            referral_link = generate_referral_link(user)
            print(referral_link)

            return render_template("index.html",
                                   static_url_path='/static',
                                   user_id=user_id,
                                   balance=balance,
                                   account_age=account_age,
                                   var_main_task=var_main_task,
                                   id_refer=id_refer,
                                   mine_friends=mine_friends,
                                   mine_pussies=mine_pussies,
                                   count_friends=count_friends,
                                   referral_link=referral_link,
                                   activity_counter=activity_counter,
                                   )
        else:
            return "Пользователь не найден."

@app.route('/update_balance/<int:user_id>', methods=['POST'])
async def update_balance(user_id):
    async with async_session() as session:
        print('обновляю')
        # Находим пользователя по user_id
        result = await session.execute(select(User).where(User.id_tg == user_id))
        user = result.scalar_one_or_none()
        if user:
            # Обновляем данные пользователя
            user.balance += 1000
            user.var_main_task = 1
            await session.commit()
            await session.slose()
            # Возвращаем ответ без сообщения
            return jsonify({'success': True})
        else:
            # Возвращаем ответ, если пользователь не найден
            return jsonify({'success': False, 'message': 'Пользователь не найден.'}), 404


@app.route('/invite/<referral_code>')
def invite(referral_code):
    # Логика обработки приглашения по реферальному коду
    return f"Invite page for referral code: {referral_code}"


def generate_referral_link(user):
    if user and user.referral_code:
        return url_for('invite', referral_code=user.referral_code, _external=True)
    return None



@app.route('/get_activity_counter/<int:user_id>', methods=['GET'])
async def get_activity_counter(user_id):
    async with async_session() as session:
        result = await session.execute(select(User).where(User.id_tg == user_id))
        user = result.scalar_one_or_none()
        if user:
            return jsonify(activity_counter=user.activity_counter)
        else:
            return jsonify(error="User not found"), 404



async def record_last_activity(user, session):
    user.last_activity_time = datetime.now()
    session.add(user)
    # await session.commit()


async def calculate_time_since_last_activity(user):
    current_time = datetime.now()
    time_since_last_activity = (current_time - user.last_activity_time).total_seconds() / 60
    return time_since_last_activity


async def update_activity_counter(user, minutes_passed):
    # Если activity_counter не задан, устанавливаем его в 0
    if user.activity_counter is None:
        user.activity_counter = 0

    # Обновляем счетчик активности
    new_counter_value = min(480, user.activity_counter + minutes_passed)
    user.activity_counter = new_counter_value

    # Сохраняем изменения в базе данных
    async with async_session() as session:
        session.add(user)
        await session.commit()


async def dynamic_points_addition(user, interval=1):  # Интервал в минутах
    while True:
        # Расчет времени с момента последней активности
        minutes_passed = await calculate_time_since_last_activity(user)

        # Обновляем счетчик активности
        await update_activity_counter(user, minutes_passed)

        # Ждем интервал перед следующим обновлением
        await asyncio.sleep(interval)


# использование
async def mining_pussies(user, session):
    if user:
        await record_last_activity(user, session)

        # Запуск фонового процесса для динамического добавления поинтов
        task = asyncio.create_task(dynamic_points_addition(user, session))

        # При выходе пользователя из приложения
        # Отменяем задачу
        task.cancel()
        await task




#
# # пока не используется. Проверить.
# def check_subscription(id_tg):
#     channel_id = "-1002211798730"
#     url = f"https://api.telegram.org/botYOUR_BOT_TOKEN/getChatMember?chat_id={channel_id}&user_id={id_tg}"
#     response = requests.get(url)
#     if response.status_code == 200:
#         data = response.json()
#         status = data['result']['status']
#         return status in ['member', 'creator']
#     print('подписка')
#     return False
#
#
# def check_subs(id_tg):
#     user = User.query.filter_by(id_tg=id_tg).first()
#     if user.var_main_task == 0:
#         if check_subscription(id_tg):
#             user.subscribed = True
#             user.balance += 1000
#             db.session.commit()
#             return True
#     return False
#
#
# def update_user_balance(id_tg):
#     user = User.query.filter_by(id_tg=id_tg).first()
#     if user and not user.subscribed:
#         if check_subscription(id_tg):
#             user.subscribed = True
#             user.balance += 1000
#             db.session.commit()
#             return True
#     return False


if __name__ == '__main__':
    try:
        app.run(ssl_context=(
            'D:\\_py_projects\\PussyCoin\\cert\\localhost.crt', 'D:\\_py_projects\\PussyCoin\\cert\\localhost.key'),
            host='0.0.0.0', port=443)
    except KeyboardInterrupt:
        print('Exit')
