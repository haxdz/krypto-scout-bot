import random

async def generate_signal(symbol):
    direction = random.choice(["Покупать", "Продавать", "Наблюдать"])
    return f"{direction} {symbol}"

async def check_market_and_notify(app):
    print("🔁 Автоматический анализ...")
    # Здесь должен быть реальный анализ и отправка сообщений
