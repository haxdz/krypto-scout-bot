from apscheduler.schedulers.asyncio import AsyncIOScheduler
from signals import generate_signal
import asyncio

scheduler = AsyncIOScheduler()

def start_scheduler(app, chat_id):
    scheduler.add_job(
        lambda: asyncio.create_task(check_market_and_notify(app, chat_id)),
        'interval',
        seconds=60  # Каждую минуту
    )
    if not scheduler.running:
        scheduler.start()

async def check_market_and_notify(app, chat_id):
    print("⏰ Уведомление отправляется!")
    for symbol in ["BTC", "ETH", "SOL"]:
        text, chart = await generate_signal(symbol)
        await app.bot.send_photo(chat_id=chat_id, photo=chart, caption=text)
