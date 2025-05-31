from apscheduler.schedulers.asyncio import AsyncIOScheduler
from signals import generate_signal
import asyncio

scheduler = AsyncIOScheduler()

def start_scheduler(app, chat_id_func):
    def job():
        loop = asyncio.get_event_loop()
        loop.create_task(check_market_and_notify(app, chat_id_func))

    scheduler.add_job(job, "interval", minutes=15)
    scheduler.start()

async def check_market_and_notify(app, chat_id_func):
    chat_id = chat_id_func()
    if chat_id is None:
        print("⚠️ chat_id пока не установлен!")
        return

    symbol = "BTC"
    signal_text, chart = await generate_signal(symbol)
    await app.bot.send_photo(chat_id=chat_id, photo=chart, caption=signal_text)
