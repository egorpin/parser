from sqlalchemy import BigInteger, ForeignKey, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, relationship, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from typing import List

import os
from dotenv import load_dotenv

load_dotenv()
engine = create_async_engine(url=os.getenv('DATABASE_URL'))

async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)
    interval_hours: Mapped[int] = mapped_column(Integer, default=0)
    _tags: Mapped["TagList"] = relationship()

    @property
    def tags(self):
        return [getattr(self._tags, f'tag{i}') for i in range(4)]

    @tags.setter
    def tags(self, tags):
        if len(tags) > 4:
            raise RuntimeWarning("Tag list can store no more than 4 tags")
        for i in range(min(4, len(tags))):
            self._tags[0] = getattr(self._tags, f'tag{i}') # это так не работает


class TagList(Base):
    __tablename__ = 'tags'

    id: Mapped[int] = mapped_column(ForeignKey('users.id'), primary_key=True)
    tag0: Mapped[str] = mapped_column(String(32), nullable=True)
    tag1: Mapped[str] = mapped_column(String(32), nullable=True)
    tag2: Mapped[str] = mapped_column(String(32), nullable=True)
    tag3: Mapped[str] = mapped_column(String(32), nullable=True)


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
