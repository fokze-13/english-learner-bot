from datetime import datetime

from sqlalchemy import Column, select, Integer, String, ARRAY, DateTime
from sqlalchemy.orm import DeclarativeBase
from database.database_config import database


class Base(DeclarativeBase):
    """Базовая модель с общими методами для всех моделей."""

    @classmethod
    async def get(cls, pk: int):
        """Получить объект по первичному ключу"""
        try:
            async with await database.get_session() as session:
                return await session.get(cls, pk)
        except Exception as e:
            print(e)

    @classmethod
    async def filter(cls, **kwargs):
        """Получить объекты, соответствующие фильтру"""
        try:
            async with await database.get_session() as session:
                stmt = select(cls).filter_by(**kwargs)
                result = await session.execute(stmt)
                return result.scalars().all()
        except Exception as e:
            print(e)

    @classmethod
    async def all(cls):
        """Получить все записи модели"""
        try:
            async with await database.get_session() as session:
                stmt = select(cls)
                result = await session.execute(stmt)
                return result.scalars().all()
        except Exception as e:
            print(e)

    async def save(self):
        """Сохранить текущий объект в базе"""
        try:
            async with await database.get_session() as session:
                session.add(self)
                await session.commit()
                await session.refresh(self)
                return self
        except Exception as e:
            print(e)

    async def delete(self):
        """Удалить текущий объект из базы"""
        try:
            async with await database.get_session() as session:
                await session.delete(self)
                await session.commit()
        except Exception as e:
            print(e)


class User(Base):
    __tablename__ = 'users'

    telegram_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    searched_words = Column(ARRAY(String))
    created_at = Column(DateTime, default=datetime.now)
    questions = Column(Integer, default=0)
    answers = Column(Integer, default=0)
