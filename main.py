from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv

from app.handlers import router
from app.database.models import async_main

import os
import asyncio
import logging

from threading import Thread
from apscheduler.schedulers.asyncio import AsyncIOScheduler

async def test():
    #code
    pass

def runSchedule():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(test, 'cron', hour=3, minute=0)
    scheduler.start()


async def main():
    await async_main()

    load_dotenv()

    bot = Bot(token=os.getenv('BOT_TOKEN'),
              default=DefaultBotProperties(parse_mode='HTML'))
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    #thread = Thread(target=runSchedule())
    #thread.start()
    asyncio.run(main())
