from apscheduler.schedulers.asyncio import AsyncIOScheduler
from signals import generate_signal

def start_scheduler(app):
    scheduler = AsyncIOScheduler()
    scheduler.add_job(lambda: scheduled_check(app), 'interval', minutes=15)
    scheduler.start()

async def scheduled_check(app):
    try:
        signal = await generate_signal("BTC")
        for chat_id in app.chat_data:
            await app.bot.send_message(chat_id=chat_id, text=f"⏱ Автосигнал:
{signal}")
    except Exception as e:
        print("Ошибка автоанализа:", e)
