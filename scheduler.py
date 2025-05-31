from apscheduler.schedulers.asyncio import AsyncIOScheduler
import asyncio
from signals import check_market_and_notify

scheduler = AsyncIOScheduler()

def start_scheduler(app, chat_id):
    scheduler.add_job(
        lambda: asyncio.create_task(check_market_and_notify(app, chat_id)),
        trigger='interval',
        minutes=1  # или 1 минута
    )
    scheduler.start()
