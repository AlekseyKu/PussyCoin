from datetime import datetime
from sqlalchemy import BigInteger, String, DateTime, JSON, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

engine = create_async_engine(url='sqlite+aiosqlite:///db.sqlite3')
async_session = async_sessionmaker(engine, expire_on_commit=False)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    id_tg = mapped_column(BigInteger)
    id_refer: Mapped[int] = mapped_column(default=0)
    first_name: Mapped[str] = mapped_column(String(25), default='')
    last_name: Mapped[str] = mapped_column(String(25), default='')
    balance: Mapped[int] = mapped_column(default=0)
    account_age: Mapped[int] = mapped_column(default=0)
    show_preloader_age: Mapped[int] = mapped_column(default=0)

    mine_friends: Mapped[int] = mapped_column(default=0)
    mine_pussies: Mapped[int] = mapped_column(default=0)

    count_friends: Mapped[int] = mapped_column(default=0)
    var_main_task: Mapped[int] = mapped_column(default=0)
    var_task_2: Mapped[int] = mapped_column(default=0)
    var_task_3: Mapped[int] = mapped_column(default=0)
    var_task_4: Mapped[int] = mapped_column(default=0)
    var_task_5: Mapped[int] = mapped_column(default=0)
    var_task_6: Mapped[int] = mapped_column(default=0)
    var_task_7: Mapped[int] = mapped_column(default=0)

    # Поля для реферальной системы
    referral_code: Mapped[str] = mapped_column(String(10), default=None)
    referred_by: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=True)  # Идентификатор пользователя, который пригласил
    referred_users: Mapped[list] = mapped_column(JSON, default=lambda: [])  # Список идентификаторов приглашенных пользователей

    # Поля для отслеживания активности (для счетчика)
    last_activity_time: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    activity_counter: Mapped[int] = mapped_column(default=0)

class Task(Base):
    __tablename__ = 'tasks'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(25))
    coins: Mapped[int] = mapped_column()
    link: Mapped[str] = mapped_column(String(50))

# Базы не используются, в БД записи уже есть
# class Mining(Base):
#     __tablename__ = 'mining'
#
#     id: Mapped[int] = mapped_column(primary_key=True)
#     name: Mapped[str] = mapped_column(String(25))
#     counter: Mapped[int] = mapped_column()
#     coins: Mapped[int] = mapped_column()
#
#
# class Counter(Base):
#     __tablename__ = 'counters'
#
#     id: Mapped[int] = mapped_column(primary_key=True)
#     user_id: Mapped[int] = mapped_column(unique=True)
#     counter: Mapped[int] = mapped_column(default=0)
#     last_updated: Mapped[str] = mapped_column(DateTime, default=datetime.now)


# async def async_main():
#     async with engine.begin() as conn:
#         # Проверяем, существуют ли столбцы, и добавляем их, если они отсутствуют
#         await add_missing_columns(conn)
#
#
# async def add_missing_columns(conn):
#     # Проверяем наличие столбцов и добавляем их, если они отсутствуют
#     columns = await conn.execute(text("PRAGMA table_info(users);"))
#     columns = [column[1] for column in columns.fetchall()]
#
#     if 'referral_code' not in columns:
#         await conn.execute(text("ALTER TABLE users ADD COLUMN referral_code TEXT DEFAULT NULL;"))
#
#     if 'referred_by' not in columns:
#         await conn.execute(text("ALTER TABLE users ADD COLUMN referred_by TEXT DEFAULT NULL;"))
#
#     if 'referred_users' not in columns:
#         await conn.execute(text("ALTER TABLE users ADD COLUMN referred_users JSON DEFAULT '[]';"))
#
#     if 'last_activity_time' not in columns:
#         await conn.execute(text("ALTER TABLE users ADD COLUMN last_activity_time DATETIME"))
#
#     if 'activity_counter' not in columns:
#         await conn.execute(text("UPDATE users SET last_activity_time = CURRENT_TIMESTAMP"))

# работающая функция без проверки отсутствующих столбцов в БД
async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
