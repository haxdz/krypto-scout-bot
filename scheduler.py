
import time
import schedule
from signals import get_analysis

# Список монет для анализа
MONITOR_SYMBOLS = [
    "BTCUSDT", "ETHUSDT", "SOLUSDT", "AVAXUSDT", "MATICUSDT", "LINKUSDT", "ARBUSDT"
]

def run_analysis():
    print("🔁 Автоанализ запущен")
    for symbol in MONITOR_SYMBOLS:
        try:
            result = get_analysis(symbol)
            print(f"[{symbol}] RSI: {result['rsi']}, Цена: {result['price']}, Объём: {result['volume_change']}%")
            if result['rsi'] < 30 and result['volume_change'] > 20:
                print(f"📢 Сигнал на покупку: {symbol}")
        except Exception as e:
            print(f"Ошибка при анализе {symbol}: {e}")

schedule.every(15).minutes.do(run_analysis)

print("⏱️ Планировщик автоанализа запущен...")
while True:
    schedule.run_pending()
    time.sleep(5)
