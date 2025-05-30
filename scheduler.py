from apscheduler.schedulers.asyncio import AsyncIOScheduler
from signals import check_market_and_notify
import asyncio

scheduler = AsyncIOScheduler()

def my_task(app):
    print("⚙️ Выполнена тестовая задача!")

def setup_jobs(app):
    scheduler.add_job(check_market_and_notify, 'interval', seconds=900, args=[app])

def start_scheduler(app):
    scheduler = AsyncIOScheduler()
    scheduler.add_job(check_market_and_notify, 'interval', seconds=900, args=[app])
    loop = asyncio.get_event_loop()
    loop.create_task(scheduler.start())
