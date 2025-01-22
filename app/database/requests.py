from app.database.models import async_session
from app.database.models import User, TagList
from sqlalchemy import select, update

from typing import Iterable


async def get_user(tg_id: int) -> User: # это не работает
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        return user


async def get_users() -> Iterable[User]: # это тоже не работает
    async with async_session() as session:
        users = await session.scalars(select(User))

        return users


async def user_exists(tg_id: int) -> bool:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        return user is not None


async def create_user(tg_id: int) -> None:
    async with async_session() as session:
        session.add(User(tg_id=tg_id))
        await session.commit()


async def update_user(user: User) -> None:
    async with async_session() as session:
        session.add(update(User).where(User.id == user.id).values(
            interval_hours=user.interval_hours))
        session.add(update(TagList).where(TagList.id == user.id).values(
            **{f'TagList.tag{i}': user.tags[i] for i in range(4)}))

        await session.commit()
