from app.database.models import async_session
from app.database.models import User, TagList
from sqlalchemy import select, update

from typing import Iterable, Tuple

async def get_userids() -> Iterable[int]:
    async with async_session() as session:
        user_ids = await session.scalars(select(User.tg_id))
        return list(user_ids)


async def get_user_info(tg_id: int) -> Tuple[int, Iterable[str]]:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        tags = await session.scalar(select(TagList).where(TagList.id == user.id))

        return user.interval_hours, tags.tags()


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
        tags.update(new_attrs['tags'])
        
        session.add(user)
        session.add(tags)

        #session.add(update(User).where(User.tg_id == tg_id).values(
        #    interval_hours=new_attrs['interval_hours']))
        #session.add(update(TagList).where(TagList.id == ).values(
        #    **{f'TagList.tag{i}': new_attrs['tags'][i] for i in range(4)}))

        await session.commit()
