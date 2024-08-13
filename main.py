import os
import asyncio
from datetime import datetime
from flask import Flask, render_template, request, jsonify, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from _back.database.models import User, async_session

# Configurations
random_token = os.urandom(12).hex()
app = Flask(__name__)
app.secret_key = random_token

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite+aiosqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


POINT_INCREMENT_INTERVAL = 1  # Interval in seconds
MAX_POINTS = 480


async def calculate_points(user: User):
    now = datetime.utcnow()
    time_diff = (now - user.last_activity_time).total_seconds()  # Calculate time difference in seconds
    additional_points = int(time_diff // POINT_INCREMENT_INTERVAL)

    # Ограничиваем количество поинтов, чтобы не превысить MAX_POINTS
    new_activity_counter = min(user.activity_counter + additional_points, MAX_POINTS)

    user.activity_counter = new_activity_counter
    user.last_activity_time = now
    return user

@app.route('/')
async def index():
    user_id = request.args.get('user_id')

    async with async_session() as session:
        result = await session.execute(select(User).where(User.id_tg == user_id))
        user = result.scalar_one_or_none()

        if user:
            user = await calculate_points(user)
            await session.commit()
            # asyncio.create_task(manage_user_activity(user))

            return render_template("index.html",
                                   user_id=user_id,
                                   balance=user.balance,
                                   account_age=user.account_age,
                                   var_main_task=user.var_main_task,
                                   id_refer=user.id_refer,
                                   mine_friends=user.mine_friends,
                                   mine_pussies=user.mine_pussies,
                                   count_friends=user.count_friends,
                                   referral_link=generate_referral_link(user),
                                   activity_counter=user.activity_counter
                                   )
        else:
            return "Пользователь не найден."


@app.route('/update_balance/<int:user_id>', methods=['POST'])
async def update_balance(user_id):
    async with async_session() as session:
        result = await session.execute(select(User).where(User.id_tg == user_id))
        user = result.scalar_one_or_none()
        if user:
            user.balance += 1000
            user.var_main_task = 1
            await session.commit()
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'message': 'Пользователь не найден.'}), 404



@app.route('/invite/<referral_code>')
def invite(referral_code):
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
            # Получаем текущее значение activity_counter
            current_activity_counter = user.activity_counter

            # Обновляем в БД
            user.mine_pussies += current_activity_counter
            user.balance += current_activity_counter
            user.activity_counter = 0

            # Сохраняем
            session.add(user)
            await session.commit()

            # Возвращаем обновленное значение mine_pussies
            return jsonify(mine_pussies=user.mine_pussies,
                           activity_counter=user.activity_counter,
                           balance=user.balance)
        else:
            return jsonify(error="User not found"), 404


#
#
# async def update_user_data(user, session):
#     user.last_activity_time = datetime.now()
#     await session.commit()
#
#
# async def calculate_minutes_since_last_activity(user):
#     current_time = datetime.now()
#     time_since_last_activity = (current_time - user.last_activity_time).total_seconds() / 60
#     return time_since_last_activity
#
#
# async def manage_user_activity(user):
#     async with async_session() as session:
#         await update_user_data(user, session)
#         while True:
#             minutes_passed = await calculate_minutes_since_last_activity(user)
#
#             # Инициализируем activity_counter, если это необходимо
#             if user.activity_counter is None:
#                 user.activity_counter = 0
#             # Обновляем значение счетчика активности
#             user.activity_counter = min(480, user.activity_counter + minutes_passed)
#             await update_user_data(user, session)
#             await asyncio.sleep(60)  # обновление каждые 60 секунд


if __name__ == '__main__':
    try:
        app.run(ssl_context=(
            'D:\\_py_projects\\PussyCoin\\cert\\localhost.crt', 'D:\\_py_projects\\PussyCoin\\cert\\localhost.key'),
            host='0.0.0.0', port=443)
    except KeyboardInterrupt:
        print("Exit Flask")
