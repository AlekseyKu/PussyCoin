from sqlalchemy import BigInteger, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

engine = create_async_engine(url='sqlite+aiosqlite:///db.sqlite3')

async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    id_tg = mapped_column(BigInteger)
    first_name: Mapped[str] = mapped_column(String(25), default='')
    last_name: Mapped[str] = mapped_column(String(25), default='')
    balance: Mapped[int] = mapped_column(default=0)
    account_age: Mapped[int] = mapped_column(default=0)
    count_friends: Mapped[int] = mapped_column(default=0)


class Mining(Base):
    __tablename__ = 'mining'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(25))
    coins: Mapped[int] = mapped_column()


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
