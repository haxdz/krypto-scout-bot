from apscheduler.schedulers.asyncio import AsyncIOScheduler
from signals import check_market_and_notify

scheduler = AsyncIOScheduler()

def setup_jobs(app):
    scheduler.add_job(
        lambda: app.create_task(check_market_and_notify(app)),
        'interval',
        seconds=30
    )
    scheduler.start()
