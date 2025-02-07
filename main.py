import os
import asyncio
import logging
from typing import Dict, Iterable
from datetime import datetime, timedelta, timezone

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv
from apscheduler.schedulers.asyncio import AsyncIOScheduler

import app.keyboards as kb
import app.config as config
import app.database.requests as rq
from app.parser import Parser, Project
from app.handlers import router
from app.database.models import async_main


async def send_projects(user_id: int, projects: Dict[str, Iterable[Project]], bot: Bot):
    interval, tags = await rq.get_user_info(user_id)

    if datetime.now(timezone.utc).hour % interval != 0:
        return
    
    for tag in tags:
        if not tag:
            continue

        for project in projects[tag]:
            if (datetime.now(timezone.utc) - project.publish_date) < timedelta(hours=interval):
                await bot.send_message(user_id, str(project), reply_markup=kb.default)


async def test(bot: Bot):
    projects_by_categories = {}
    for category in config.categories:
        projects_by_categories[category] = Parser.parse_category_rss(category)

    user_ids = await rq.get_userids()

    for id in user_ids:
        await send_projects(id, projects_by_categories, bot)


def runSchedule(bot: Bot):
    scheduler = AsyncIOScheduler()
    scheduler.add_job(test, 'cron', args=(bot,), minute=0)  # every hour
    scheduler.start()


async def main():
    await async_main()

    load_dotenv()

    bot = Bot(token=os.getenv('BOT_TOKEN'),
              default=DefaultBotProperties(parse_mode='HTML'))

    runSchedule(bot)

    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s:%(levelname)s:%(name)s:%(message)s")
    asyncio.run(main())