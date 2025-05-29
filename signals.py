import random

async def generate_signal(symbol: str) -> str:
    rsi = random.randint(20, 80)
    volume = random.uniform(-40, 40)
    price = random.randint(500, 2000)
    signal = (
        f"🔹 RSI: {rsi}\n"
        f"🔹 Объём: {volume:.2f}% к среднему\n"
        f"🔹 Текущая цена: ${price}"
    )
    return signal
