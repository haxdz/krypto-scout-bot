import aiohttp
import pandas as pd
import matplotlib.pyplot as plt
import io
import random

BINANCE_API_URL = "https://api.binance.com/api/v3/klines"

async def check_market_and_notify(app, chat_id):
    text_signal, chart = await generate_signal("BTC")  # Пример для BTC
    await app.bot.send_photo(chat_id=chat_id, photo=chart, caption=text_signal)


# Получение исторических данных (OHLCV)
async def get_klines(symbol: str, interval: str = "1h", limit: int = 100):
    url = f"{BINANCE_API_URL}?symbol={symbol.upper()}USDT&interval={interval}&limit={limit}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
    df = pd.DataFrame(data, columns=[
        "time", "open", "high", "low", "close", "volume",
        "close_time", "quote_asset_volume", "number_of_trades",
        "taker_buy_base_asset_volume", "taker_buy_quote_asset_volume", "ignore"
    ])
    df["close"] = df["close"].astype(float)
    df["time"] = pd.to_datetime(df["time"], unit="ms")
    return df

# RSI
def calculate_rsi(prices, window=14):
    delta = prices.diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=window).mean()
    avg_loss = loss.rolling(window=window).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

# EMA
def calculate_ema(prices, span=14):
    return prices.ewm(span=span, adjust=False).mean()

# MACD
def calculate_macd(prices, slow=26, fast=12, signal=9):
    ema_fast = prices.ewm(span=fast, adjust=False).mean()
    ema_slow = prices.ewm(span=slow, adjust=False).mean()
    macd_line = ema_fast - ema_slow
    signal_line = macd_line.ewm(span=signal, adjust=False).mean()
    return macd_line, signal_line

# Bollinger Bands
def calculate_bollinger_bands(prices, window=20, num_std=2):
    rolling_mean = prices.rolling(window=window).mean()
    rolling_std = prices.rolling(window=window).std()
    upper_band = rolling_mean + (rolling_std * num_std)
    lower_band = rolling_mean - (rolling_std * num_std)
    return rolling_mean, upper_band, lower_band

# Генерация сигнала и графика
async def generate_signal(symbol: str):
    df = await get_klines(symbol, interval="1h", limit=100)
    prices = df["close"]

    # Вычисляем все индикаторы
    rsi = calculate_rsi(prices).iloc[-1]
    ema = calculate_ema(prices).iloc[-1]
    macd_line, signal_line = calculate_macd(prices)
    macd = macd_line.iloc[-1]
    macd_signal = signal_line.iloc[-1]
    ma, upper_band, lower_band = calculate_bollinger_bands(prices)
    last_price = prices.iloc[-1]

    # Логика сигнала
    if rsi < 30 and last_price < ema:
        action = "Покупать"
    elif rsi > 70 and last_price > ema:
        action = "Продавать"
    else:
        action = "Наблюдать"

    # Текстовый сигнал
    text_signal = (
        f"📊 Сигнал по {symbol.upper()}:\n"
        f"Цена: {last_price} USDT\n"
        f"RSI: {rsi:.2f}\n"
        f"EMA: {ema:.2f}\n"
        f"MACD: {macd:.2f} / Сигнальная линия: {macd_signal:.2f}\n"
        f"Рекомендация: {action}"
    )

    # График
    plt.figure(figsize=(10, 5))
    plt.plot(df["time"], prices, label="Цена", color="blue")
    plt.plot(df["time"], ma, label="MA", color="orange")
    plt.fill_between(df["time"], upper_band, lower_band, color="gray", alpha=0.2, label="Bollinger Bands")
    plt.title(f"{symbol.upper()} Анализ")
    plt.xlabel("Время")
    plt.ylabel("Цена")
    plt.legend()
    plt.grid(True)

    # Сохраняем график в памяти
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    plt.close()

    return text_signal, buf
