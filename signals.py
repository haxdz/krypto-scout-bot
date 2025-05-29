
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from binance.client import Client
import os

api_key = os.getenv("BINANCE_API_KEY")
api_secret = os.getenv("BINANCE_SECRET")

client = Client(api_key, api_secret)

def get_klines(symbol="BTCUSDT", interval="1h", limit=100):
    data = client.get_klines(symbol=symbol, interval=interval, limit=limit)
    df = pd.DataFrame(data, columns=[
        'timestamp', 'open', 'high', 'low', 'close', 'volume',
        'close_time', 'quote_asset_volume', 'number_of_trades',
        'taker_buy_base', 'taker_buy_quote', 'ignore'
    ])
    df['close'] = df['close'].astype(float)
    df['volume'] = df['volume'].astype(float)
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('timestamp', inplace=True)
    return df

def compute_rsi(prices, period=14):
    delta = prices.diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

def get_analysis(symbol="BTCUSDT"):
    df = get_klines(symbol)
    df['RSI'] = compute_rsi(df['close'])
    df['MA20'] = df['close'].rolling(window=20).mean()
    df['std'] = df['close'].rolling(window=20).std()
    df['lower_band'] = df['MA20'] - 2 * df['std']
    df['upper_band'] = df['MA20'] + 2 * df['std']
    rsi = round(df['RSI'].iloc[-1], 2)
    close = round(df['close'].iloc[-1], 2)
    lower_band = round(df['lower_band'].iloc[-1], 2)
    volume = df['volume'].iloc[-12:]
    volume_change = round((volume[-1] - volume.mean()) / volume.mean() * 100, 2)
    return {
        "symbol": symbol,
        "rsi": rsi,
        "price": close,
        "lower_band": lower_band,
        "volume_change": volume_change,
    }

def make_chart(df, symbol="BTCUSDT"):
    fig, ax1 = plt.subplots(figsize=(10, 5))
    ax1.plot(df.index, df['close'], label='Цена', linewidth=2)
    ax2 = ax1.twinx()
    ax2.plot(df.index, df['RSI'], color='red', linestyle='--', label='RSI')
    ax2.axhline(30, color='gray', linestyle=':')
    ax2.axhline(70, color='gray', linestyle=':')
    plt.title(f"{symbol} — Цена и RSI")
    fig.tight_layout()
    path = f"{symbol}_chart.png"
    plt.savefig(path)
    plt.close()
    return path
