import os
import asyncio
from datetime import datetime
from flask import Flask, render_template, request, jsonify, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

# Configurations
random_token = os.urandom(12).hex()
app = Flask(__name__)
app.secret_key = random_token

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite+aiosqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
engine = create_async_engine(app.config['SQLALCHEMY_DATABASE_URI'])
async_session = async_sessionmaker(engine, expire_on_commit=False)


@app.route('/')
async def index():
	user_id = request.args.get('user_id')

	async with async_session() as session:
		result = await session.execute(select(User).where(User.id_tg == user_id))
		user = result.scalar_one_or_none()

		if user:
			asyncio.create_task(manage_user_activity(user))

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
			return jsonify(activity_counter=user.activity_counter)
		else:
			return jsonify(error="User not found"), 404


async def update_user_data(user, session):
	user.last_activity_time = datetime.now()
	await session.commit()


async def calculate_minutes_since_last_activity(user):
	current_time = datetime.now()
	time_since_last_activity = (current_time - user.last_activity_time).total_seconds() / 60
	return time_since_last_activity


async def manage_user_activity(user):
	async with async_session() as session:
		await update_user_data(user, session)
		while True:
			minutes_passed = await calculate_minutes_since_last_activity(user)
			user.activity_counter = min(480, user.activity_counter + minutes_passed)
			await update_user_data(user, session)
			await asyncio.sleep(60)  # обновление каждые 60 секунд


if __name__ == '__main__':
	app.run(ssl_context=(
		'path/to/localhost.crt', 'path/to/localhost.key'),
		host='0.0.0.0', port=443)

# import asyncio
# from datetime import datetime
#
#
# async def increment_counter(counter):
# 	while counter < 480:
# 		await asyncio.sleep(1)  # Ждем 60 секунд (1 минуту)
# 		counter += 1
# 		progress = counter / 480
# 		print(f"Progress: {progress:.2%} ({counter}/480)")
# 	print("Максимальное значение счетчика достигнуто.")
#
#
# async def main():
# 	counter = 0
# 	await increment_counter(counter)
#
#
# if __name__ == "__main__":
# 	asyncio.run(main())
