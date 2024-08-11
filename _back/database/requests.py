from sqlalchemy import select

from _back.database.models import async_session
from _back.database.models import User, Mining
from _back.database.query import account_age as get_account_age


async def set_user(id_tg, first_name, last_name):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.id_tg == id_tg))
        
        if not user:
            user_account_age = get_account_age()
            session.add(User(id_tg=id_tg, first_name=first_name, last_name=last_name,
                             account_age=user_account_age, balance=user_account_age,
                             count_friends=0, var_main_task=0))
            await session.commit()

        # if user.first_name != first_name or user.last_name != last_name:
        #     user.first_name = first_name
        #     user.last_name = last_name
        #     await session.commit()
        #
        #     # TODO потестить. Если изменилось имя/фамилия
        #
        # else:
        #     user_account_age = get_account_age()
        #     session.add(User(id_tg=id_tg, first_name=first_name, last_name=last_name, account_age=user_account_age))
        #     await session.commit()



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