from app.database.models import async_session
from app.database.models import User, TagList
from sqlalchemy import select, update

from typing import Iterable


async def get_user(tg_id: int) -> User: # это не работает
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        return user

"""
async def get_users() -> Iterable[User]: # это тоже не работает
    async with async_session() as session:
        users = await session.scalars(select(User))

        return users
"""

async def user_exists(tg_id: int) -> bool:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        return user is not None


async def create_user(tg_id: int) -> None:
    async with async_session() as session:
        user = User(tg_id=tg_id)
        user._tags = TagList()

        session.add(user)
        await session.commit()


async def update_user(tg_id: int, **new_attrs) -> None:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        tags = await session.scalar(select(TagList).where(TagList.id == user.id))

        user.interval_hours = new_attrs['interval_hours']
        for i in range(min(len(new_attrs['tags']), 4)):
            setattr(tags, f'tag{i}', new_attrs['tags'][i])
        
        session.add(user)
        session.add(tags)

        #session.add(update(User).where(User.tg_id == tg_id).values(
        #    interval_hours=new_attrs['interval_hours']))
        #session.add(update(TagList).where(TagList.id == ).values(
        #    **{f'TagList.tag{i}': new_attrs['tags'][i] for i in range(4)}))

        await session.commit()
