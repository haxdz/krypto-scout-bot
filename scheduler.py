from apscheduler.schedulers.asyncio import AsyncIOScheduler
from signals import generate_signal
import asyncio
from bot import chat_id  # импортируем chat_id

scheduler = AsyncIOScheduler()

async def check_market_and_notify(app):
    if chat_id is None:
        print("⚠️ chat_id пока не установлен!")
        return

    symbol = "BTC"  # или список монет для анализа
    signal_text, chart = await generate_signal(symbol)
    await app.bot.send_photo(chat_id=chat_id, photo=chart, caption=signal_text)

def start_scheduler(app):
    scheduler.add_job(
        lambda: asyncio.create_task(check_market_and_notify(app)),
        "interval",
        minutes=15
    )
    scheduler.start()
