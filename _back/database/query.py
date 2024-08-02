from random import random, randint
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from werkzeug.utils import redirect

import requests

from flask import session, current_app, jsonify, url_for

from _back.database.models import User

DATABASE_URL = 'sqlite:///db.sqlite3'

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

def account_age():
    result = randint(2000, 7000)
    return result


def get_account_info_from_db(id_tg):
    user = session.query(User).filter_by(id_tg=id_tg).first()
    if user:
        balance = user.balance
        account_age = user.account_age
    else:
        balance = None
        account_age = None
    session.close()
    return balance, account_age



async def process_tg_user_id(tg_user_id):
    print({'id_tg': tg_user_id})









# Обновление БД после проверки на подписку канала в tg

# def check_subs(id_tg):
#     user = session.query(User).filter_by(id_tg=id_tg).first()
#     if user.var_task_main == 0:
#         user.var_task_main = 1
#         user.balance += 1000
#         session.commit()
#         session.close()
#         return redirect('https://t.me/+8K1Wfb_o_3NhNjk1')
#     return redirect('https://t.me/+8K1Wfb_o_3NhNjk1')



def check_sub(id_tg):
    session = Session()
    user = session.query(User).filter_by(id_tg=id_tg).first()
    if user.var_task_main == 0:
        update_database(id_tg)
    else:
        pass
        
def update_database(id_tg):
    session = Session()
    user = session.query(User).filter_by(id_tg=id_tg).first()
    user.var_task_main = 1
    user.balance += 1000
    print('обновление базы данных')
    session.commit()
    session.close()










#
# from random import random, randint
# from sqlalchemy import create_engine, select
# from sqlalchemy.orm import sessionmaker
# import requests
#
# from flask import session, current_app, jsonify
#
# from _back.database.models import User
#
# DATABASE_URL = 'sqlite:///db.sqlite3'
#
# engine = create_engine(DATABASE_URL)
# Session = sessionmaker(bind=engine)
#
#
# def account_age():
#     result = randint(2000, 7000)
#     return result
#
#
# def get_account_info_from_db(id_tg):
#     session = Session()
#     user = session.query(User).filter_by(id_tg=id_tg).first()
#     if user:
#         balance = user.balance
#         account_age = user.account_age
#     else:
#         balance = None
#         account_age = None
#     session.close()
#     return balance, account_age
#
#
# # Обновление БД после проверки на подписку канала в tg
#
# def check_sub(id_tg):
#     session = Session()
#     user = session.query(User).filter_by(id_tg=id_tg).first()
#     if user.var_task_main == 0:
#         update_database(id_tg)
#     else:
#         pass
#
#
# def update_database(id_tg):
#     session = Session()
#     user = session.query(User).filter_by(id_tg=id_tg).first()
#     user.var_task_main = 1
#     user.balance += 1000
#     print('обновление базы данных')
#     session.commit()
#     session.close()










# def check_subscription(id_tg):
#     session = Session()
#     tg_id = session.query(User).filter_by(id_tg=id_tg).first()
#     url = f'https://t.me/+8K1Wfb_o_3NhNjk1'
#     response = requests.get(url)
#     data = response.json()
#     is_subscribed = data['result']['status'] == 'member'
#
#     if is_subscribed:
#         user = User.query.filter_by(tg_id=tg_id).first()
#         if user:
#             user.var_task_main = 1
#             user.balance += 1000
#             session.commit()
#
#     return jsonify({'is_subscribed': is_subscribed})


# Работающие варианты. обЪединены в get_account_info_from_DB
# def get_user_balance(id_tg):
#     session = Session()
#     user = session.query(User).filter_by(id_tg=id_tg).first()
#     if user:
#         balance = user.balance
#     else:
#         balance = None
#     session.close()
#     return balance

# def get_account_age(id_tg):
#     session = Session()
#     user = session.query(User).filter_by(id_tg=id_tg).first()
#     if user:
#         account_age = user.account_age
#     else:
#         account_age = None
#     session.close()
#     return account_age


# get_tg_id from DB by num
# def get_tg_id():
#     with Session(autoflush=False, bind=engine) as db:
#         info = db.get(User, 1)  # current_user_id
#         data = info.balance
#         print(data)
#         return data


# Stack: Python Aiogram 3 (бот telegram), Flask (webapp), Sqlite+Sqlalchemy
# Deploy: vps Ubuntu 20.04, Node+Express

# Что было сделано: 
# С помощью aiogram получаем telegram id текущего пользователя (massage.from_user.id), 
# который будет использован для дальнейших обработок, 
# в том числе На его основании подтягивать из БД динамически внесенную информацию.

# Пробовал варианты передачи:
# 1. через global-переменную 
# 2. через FSMContext
# 3. Запись переменной в отдельный процесс multiprocessing 
# Во всех случаях выводит None

# Задача: 
# Необходимо передать telegram id текущего пользователя, текущей сессии из модуля haldlers.py (aiogram 3) 
# в app.py (Flask)


# TODO: # Postgres - заменить sqlite
# telegram api - проверка на пользователя


#______________________________________________TEST CODE_____________
# current_user_id = get_current_user_id()
# get_current_user_id()

# последний вариант
# def get_tg_id():
#     with Session(autoflush=False, bind=engine) as db:
#         current_user_id = 
#         info = db.get(User, current_user_id) # current_user_id
#         data = info.balance 
#         print(data)
#         return data

# Проба
# def get_tg_id(id_tg):
#     with Session(autoflush=False, bind=engine) as db:
#  # Получаем пользователя по id_tg
#         stmt = select(User).where(User.id_tg == id_tg)
#         user = db.execute(stmt).scalar_one_or_none()

#         if user is None:
#             print("User not found")
#             return None

#         current_user_id = user.id
#         info = db.get(User, current_user_id)
#         data = info.balance

#         print(data)
#         return data

# TODO: 1 = current_user_id

# # ! backup function
# def get_tg_id():
#     with Session(autoflush=False, bind=engine) as db:
#         info = db.get(User, 1) # current_user_id
#         data = info.balance 
#         print(data)
#         return data


# current_user_id = await state.get_data('current_user_id')
# return current_user_id


# def get_user_balance(id_tg, state: FSMContext):
#     """Функция для получения имени пользователя."""
#
#
#     session = Session()
#     try:
#         # запрос для получения баланса пользователя
#         query = select(User.balance).where(User.id_tg == id_tg)
#         result = session.execute(query)
#         balance = result.scalar()
#         return balance
#     finally:
#         session.close()  # Закрытие сессии
#
#
# async def get_current_id(state: FSMContext):
#     data = await state.get_data()
#     return data


# tg.initDataUnsafe.user.id
