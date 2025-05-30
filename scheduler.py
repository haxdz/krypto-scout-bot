from apscheduler.schedulers.asyncio import AsyncIOScheduler
from signals import check_market_and_notify

scheduler = AsyncIOScheduler()

def setup_jobs(app):
    scheduler.add_job(check_market_and_notify, 'interval', seconds=900, args=[app])

def start_scheduler(app):
    scheduler = AsyncIOScheduler()
    scheduler.add_job(my_task, 'interval', seconds=10, args=[app])
    scheduler.start()
