from random import randint
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


from flask import session

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
