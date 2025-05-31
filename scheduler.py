from apscheduler.schedulers.asyncio import AsyncIOScheduler
import asyncio

scheduler = AsyncIOScheduler()

def start_scheduler(app, chat_id):
    async def dummy_task():
        print(f"✅ Задача выполнена для {chat_id}!")  # это в логи выведется
        await app.bot.send_message(chat_id=chat_id, text="⏰ Это тестовое уведомление от планировщика!")

    scheduler.add_job(lambda: asyncio.create_task(dummy_task()), trigger='interval', seconds=60)
    scheduler.start()
