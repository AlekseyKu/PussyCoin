import os
from datetime import datetime
from flask import Flask, render_template, request, jsonify
# from flask_csp import CSP
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.future import select

from _back.database.models import User, Task, async_session

# Configurations
random_token = os.urandom(12).hex()
app = Flask(__name__)
app.secret_key = random_token

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite+aiosqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


@app.after_request
def apply_csp(response):
    response.headers['Content-Security-Policy'] = "frame-src http: https: https://t.me tg://"
    return response


@app.route('/')
async def index():
    user_id = request.args.get('user_id')

    async with async_session() as session:
        result = await session.execute(select(User).where(User.id_tg == user_id))
        user = result.scalar_one_or_none()
        # result_tasks = await session.execute(select(Task))
        # tasks = result_tasks.scalars().all()

        task_ids = [1, 2, 3, 4, 5, 6, 7]
        result_tasks = await session.execute(
            select(Task).where(Task.id.in_(task_ids))
        )
        tasks = result_tasks.scalars().all()

        tasks_dict = {f'task_{task.id}': task for task in tasks}

        referral_bonuses = 0

        if user:
            if user.referred_users:
                referral_bonuses = sum(referral.get('bonus', 0) for referral in user.referred_users)

            user = await calculate_points(user)
            await session.commit()

            return render_template("index.html",
                                   user_id=user_id,
                                   balance=user.balance,
                                   account_age=user.account_age,
                                   show_preloader_age=user.show_preloader_age,
                                   id_refer=user.id_refer,
                                   mine_friends=user.mine_friends,
                                   mine_pussies=user.mine_pussies,
                                   count_friends=user.count_friends,
                                   activity_counter=user.activity_counter,
                                   referral_bonuses=referral_bonuses,

                                   var_main_task=user.var_main_task,
                                   var_task_2=user.var_task_2,
                                   var_task_3=user.var_task_3,
                                   var_task_4=user.var_task_4,
                                   var_task_5=user.var_task_5,
                                   var_task_6=user.var_task_6,
                                   var_task_7=user.var_task_7,
                                   **tasks_dict
                                   )
        else:
            return "Пользователь не найден."


@app.route('/var_main_task/<int:user_id>', methods=['POST'])
async def update_balance(user_id):
    async with async_session() as session:
        result = await session.execute(select(User).where(User.id_tg == user_id))
        user = result.scalar_one_or_none()
        if user:
            user.balance += 2000
            user.var_main_task = 1
            await session.commit()
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'message': 'Пользователь не найден.'}), 404

@app.route('/var_task_2/<int:user_id>', methods=['POST'])
async def var_task_2(user_id):
    async with async_session() as session:
        result = await session.execute(select(User).where(User.id_tg == user_id))
        user = result.scalar_one_or_none()
        if user:
            user.balance += 1500
            user.var_task_2 = 1
            await session.commit()
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'message': 'Пользователь не найден.'}), 404

@app.route('/var_task_3/<int:user_id>', methods=['POST'])
async def var_task_3(user_id):
    async with async_session() as session:
        result = await session.execute(select(User).where(User.id_tg == user_id))
        user = result.scalar_one_or_none()
        if user:
            user.balance += 1500
            user.var_task_3 = 1
            await session.commit()
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'message': 'Пользователь не найден.'}), 404


@app.route('/var_task_4/<int:user_id>', methods=['POST'])
async def var_task_4(user_id):
    async with async_session() as session:
        result = await session.execute(select(User).where(User.id_tg == user_id))
        user = result.scalar_one_or_none()
        if user:
            user.balance += 2000
            user.var_task_4 = 1
            await session.commit()
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'message': 'Пользователь не найден.'}), 404


@app.route('/var_task_5/<int:user_id>', methods=['POST'])
async def var_task_5(user_id):
    async with async_session() as session:
        result = await session.execute(select(User).where(User.id_tg == user_id))
        user = result.scalar_one_or_none()
        if user:
            user.balance += 1700
            user.var_task_5 = 1
            await session.commit()
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'message': 'Пользователь не найден.'}), 404


@app.route('/var_task_6/<int:user_id>', methods=['POST'])
async def var_task_6(user_id):
    async with async_session() as session:
        result = await session.execute(select(User).where(User.id_tg == user_id))
        user = result.scalar_one_or_none()
        if user:
            user.balance += 2000
            user.var_task_6 = 1
            await session.commit()
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'message': 'Пользователь не найден.'}), 404

@app.route('/var_task_7/<int:user_id>', methods=['POST'])
async def var_task_7(user_id):
    async with async_session() as session:
        result = await session.execute(select(User).where(User.id_tg == user_id))
        user = result.scalar_one_or_none()
        if user:
            user.balance += 2000
            user.var_task_7 = 1
            await session.commit()
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'message': 'Пользователь не найден.'}), 404

# PRELOADER
@app.route('/update-preloader-age/<int:user_id>', methods=['POST'])
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
@app.route('/generate_referral_link')
async def generate_referral_link():
    user_id = request.args.get('user_id')

    async with async_session() as session:
        result = await session.execute(select(User).where(User.id_tg == user_id))
        user = result.scalar_one_or_none()
        if user:
            referral_link = f"https://t.me/PussyCoinCommunityBot?start={user.referral_code}"
            # referral_link = f"https://t.me/pussycoin_test_bot?start={user.referral_code}"
            print(referral_link)
            return jsonify({'referral_link': referral_link})
        else:
            return jsonify({'error': 'Ошибка при генерации реферального кода'}), 500



@app.route('/invite/<referral_text>')
def invite(referral_text):
    return f"We eat, sleep and mine pussies. Non-stop. And you? Join US!!! {referral_text}"


@app.route('/referrals/<int:user_id>')
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
async def calculate_points(user: User):
    now = datetime.utcnow()
    time_diff = (now - user.last_activity_time).total_seconds()  # Calculate time difference in seconds
    additional_points = int(time_diff // 60)
    print(additional_points)

    new_activity_counter = min(user.activity_counter + additional_points, 480)
    print(new_activity_counter)

    # start_var_timer = 480
    # new_timer =

    user.activity_counter = new_activity_counter
    user.last_activity_time = now
    return user


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


@app.route('/get_and_update_activity_counter/<int:user_id>', methods=['GET'])
async def get_and_update_activity_counter(user_id):
    async with async_session() as session:
        result = await session.execute(select(User).where(User.id_tg == user_id))
        user = result.scalar_one_or_none()

        if user:
            # Обновляем activity_counter с использованием calculate_points
            user = await calculate_points(user)
            await session.commit()

            # Возвращаем текущее значение activity_counter
            return jsonify(activity_counter=user.activity_counter)
        else:
            return jsonify(error="User not found"), 404



# if __name__ == '__main__':
#     try:
#         app.run(ssl_context=(
#             'D:\\_py_projects\\PussyCoin\\cert\\localhost.crt', 'D:\\_py_projects\\PussyCoin\\cert\\localhost.key'),
#             host='0.0.0.0', port=443)
#     except KeyboardInterrupt:
#         print("Exit Flask")

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=443)
    except KeyboardInterrupt:
        print("Exit Flask")
