import secrets
from sqlalchemy import select

from _back.database.models import async_session
from _back.database.models import User
from _back.database.query import account_age as get_account_age


async def set_user(id_tg, first_name, last_name):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.id_tg == id_tg))
        
        if not user:
            user_account_age = get_account_age()
            referral_code = secrets.token_hex(4)
            session.add(User(
                id_tg=id_tg,
                first_name=first_name,
                last_name=last_name,
                account_age=user_account_age,
                balance=user_account_age,
                count_friends=0,
                var_main_task=0,
                referral_code=referral_code,  # Добавлен реферальный код
                referred_by=None,  # Новый пользователь не приглашен никем
                referred_users=[]  # Список приглашенных пользователей пуст
            ))
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
