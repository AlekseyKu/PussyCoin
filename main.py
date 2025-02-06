import os
from datetime import datetime
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.future import select
from pathlib import Path

from _back.database.models import User, Task, async_session

# Configurations
random_token = os.urandom(12).hex()
app = Flask(__name__, static_url_path='/pussycoin/static', static_folder='static')
app.secret_key = random_token

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite+aiosqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


@app.after_request
def apply_csp(response):
    response.headers['Content-Security-Policy'] = "frame-src http: https: https://t.me tg://"
    return response


@app.route('/pussycoin')
# @app.route('/')
async def index():
    user_id = request.args.get('user_id')

    async with async_session() as session:
        result = await session.execute(select(User).where(User.id_tg == user_id))
        user = result.scalar_one_or_none()
        # result_tasks = await session.execute(select(Task))
        # tasks = result_tasks.scalars().all()

        task_ids = [1, 2, 3, 4]
        result_tasks = await session.execute(
            select(Task).where(Task.id.in_(task_ids))
        )
        tasks = result_tasks.scalars().all()

        tasks_dict = {f'task_{task.id}': task for task in tasks}

        referral_bonuses = 0

        rounded_activity_counter = round(user.activity_counter, 5)
        rounded_balance = round(user.balance, 5)
        print(f"Rounded activity counter: {rounded_activity_counter}")

        if user:
            if user.referred_users:
                referral_bonuses = sum(referral.get('bonus', 0) for referral in user.referred_users)

            user = await calculate_points(user)
            await session.commit()
            print(rounded_balance)

            return render_template("index.html",
                                   user_id=user_id,
                                   balance=rounded_balance,
                                   account_age=user.account_age,
                                   show_preloader_age=user.show_preloader_age,
                                   id_refer=user.id_refer,
                                   mine_friends=user.mine_friends,
                                   mine_pussies=round(user.mine_pussies,5),
                                   count_friends=user.count_friends,
                                   activity_counter=rounded_activity_counter,
                                   referral_bonuses=referral_bonuses,

                                   var_main_task=user.var_main_task,
                                   var_task_2=user.var_task_2,
                                   var_task_3=user.var_task_3,
                                   var_task_4=user.var_task_4,
                                   # var_task_5=user.var_task_5,
                                   # var_task_6=user.var_task_6,
                                   # var_task_7=user.var_task_7,
                                   **tasks_dict
                                   )
        else:
            return "Пользователь не найден."


@app.route('/api/var_main_task/<int:user_id>', methods=['POST'])
async def update_balance(user_id):
    async with async_session() as session:
        result = await session.execute(select(User).where(User.id_tg == user_id))
        user = result.scalar_one_or_none()
        if user:
            user.balance += 0.3
            user.var_main_task = 1
            await session.commit()
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'message': 'Пользователь не найден.'}), 404

@app.route('/api/var_task_2/<int:user_id>', methods=['POST'])
async def var_task_2(user_id):
    async with async_session() as session:
        result = await session.execute(select(User).where(User.id_tg == user_id))
        user = result.scalar_one_or_none()
        if user:
            user.balance += 0.3
            user.var_task_2 = 1
            await session.commit()
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'message': 'Пользователь не найден.'}), 404

@app.route('/api/var_task_3/<int:user_id>', methods=['POST'])
async def var_task_3(user_id):
    async with async_session() as session:
        result = await session.execute(select(User).where(User.id_tg == user_id))
        user = result.scalar_one_or_none()
        if user:
            user.balance += 0.3
            user.var_task_3 = 1
            await session.commit()
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'message': 'Пользователь не найден.'}), 404


@app.route('/api/var_task_4/<int:user_id>', methods=['POST'])
async def var_task_4(user_id):
    async with async_session() as session:
        result = await session.execute(select(User).where(User.id_tg == user_id))
        user = result.scalar_one_or_none()
        if user:
            user.balance += 0.3
            user.var_task_4 = 1
            await session.commit()
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'message': 'Пользователь не найден.'}), 404


# @app.route('/var_task_5/<int:user_id>', methods=['POST'])
# async def var_task_5(user_id):
#     async with async_session() as session:
#         result = await session.execute(select(User).where(User.id_tg == user_id))
#         user = result.scalar_one_or_none()
#         if user:
#             user.balance += 1700
#             user.var_task_5 = 1
#             await session.commit()
#             return jsonify({'success': True})
#         else:
#             return jsonify({'success': False, 'message': 'Пользователь не найден.'}), 404
#
#
# @app.route('/var_task_6/<int:user_id>', methods=['POST'])
# async def var_task_6(user_id):
#     async with async_session() as session:
#         result = await session.execute(select(User).where(User.id_tg == user_id))
#         user = result.scalar_one_or_none()
#         if user:
#             user.balance += 2000
#             user.var_task_6 = 1
#             await session.commit()
#             return jsonify({'success': True})
#         else:
#             return jsonify({'success': False, 'message': 'Пользователь не найден.'}), 404
#
# @app.route('/var_task_7/<int:user_id>', methods=['POST'])
# async def var_task_7(user_id):
#     async with async_session() as session:
#         result = await session.execute(select(User).where(User.id_tg == user_id))
#         user = result.scalar_one_or_none()
#         if user:
#             user.balance += 2000
#             user.var_task_7 = 1
#             await session.commit()
#             return jsonify({'success': True})
#         else:
#             return jsonify({'success': False, 'message': 'Пользователь не найден.'}), 404

# PRELOADER
@app.route('/api/update-preloader-age/<int:user_id>', methods=['POST'])
async def update_preloader_age(user_id):
    async with async_session() as session:
        result = await session.execute(select(User).where(User.id_tg == user_id))
        user = result.scalar_one_or_none()
        if user:
            user.show_preloader_age = 1
            await session.commit()
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'message': 'Пользователь не найден.'}), 404


# REFERRALS
@app.route('/api/generate_referral_link')
async def generate_referral_link():
    user_id = request.args.get('user_id')

    async with async_session() as session:
        result = await session.execute(select(User).where(User.id_tg == user_id))
        user = result.scalar_one_or_none()
        if user:
            # referral_link = f"https://t.me/PussyCoinCommunityBot?start={user.referral_code}"
            referral_link = f"https://t.me/DomesticDuckBot?start={user.referral_code}"
            print(referral_link)
            return jsonify({'referral_link': referral_link})
        else:
            return jsonify({'error': 'Ошибка при генерации реферального кода'}), 500



@app.route('/api/invite/<referral_text>')
def invite(referral_text):
    return f"We eat, sleep and mine $DDUCK. Non-stop. And you? Join US!!! {referral_text}"


@app.route('/api/referrals/<int:user_id>')
async def get_referrals(user_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.id_tg == user_id))
        if user:
            referrals = user.referred_users
            referral_list = [
                {'name': referral['name'], 'bonus': referral['bonus'], 'ava': num + 1}
                for num, referral in enumerate(referrals)
            ]
            return jsonify(referral_list)
        else:
            return jsonify({'error': 'Пользователь не найден'}), 404




# POINTS
async def calculate_points(user):
    now = datetime.utcnow()
    time_diff = (now - user.last_activity_time).total_seconds()  # Разница во времени в секундах

    # Расчет дополнительных очков: 0.05 каждый час
    additional_points = round((time_diff * 0.05) / 3600, 5)  # Перевод в часы, округление до стотысячной
    additional_points = min(additional_points, 0.05)  # Максимум 0.05 в час

    # print(f"Time diff (seconds): {time_diff}")
    # print(f"Additional points: {additional_points}")

    # Обновление счётчика активности с учетом лимита 0.5
    new_activity_counter = round(min(user.activity_counter + additional_points, 0.3), 5)

    # Логика сброса очков, если достигнуто 0.3
    if new_activity_counter >= 0.3:
        print(f"Activity counter reached the maximum value and will be reset. Current: {new_activity_counter}")
        new_activity_counter = 0  # Сбрасываем счетчик


    # Обновление пользователя
    user.activity_counter = new_activity_counter
    user.last_activity_time = now

    return user


@app.route('/api/get_activity_counter/<int:user_id>', methods=['GET'])
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


@app.route('/api/get_and_update_activity_counter/<int:user_id>', methods=['GET'])
async def get_and_update_activity_counter(user_id):
    async with async_session() as session:
        result = await session.execute(select(User).where(User.id_tg == user_id))
        user = result.scalar_one_or_none()

        if user:
            # Обновляем activity_counter с использованием calculate_points
            user = await calculate_points(user)
            await session.commit()

            # Возвращаем текущее значение activity_counter
            return jsonify(activity_counter=round(user.activity_counter, 5))
        else:
            return jsonify(error="User not found"), 404



# if __name__ == '__main__':
#     print(f'{Path(__file__).parent}/cert/localhost.crt')
#     try:
#         app.run(ssl_context=(
#             f'{Path(__file__).parent}/cert/localhost.crt', f'{Path(__file__).parent}/cert/localhost.key'),
#             host='0.0.0.0', port=443)
#     except KeyboardInterrupt:
#         print("Exit Flask")

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=8000)
    except KeyboardInterrupt:
        print("Exit Flask")