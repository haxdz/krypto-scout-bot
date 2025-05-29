from telegram.ext import Defaults
import logging
logging.basicConfig(level=logging.INFO)


import os
import time
import schedule
import threading

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputFile
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

from signals import get_analysis, get_klines, compute_rsi, make_chart

BOT_TOKEN = os.getenv("BOT_TOKEN")

# Telegram logic
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я Krypto Scout 🤖\nКаждые 15 минут я сканирую рынок.\nКоманды:\n/check — ручной анализ\n/portfolio — отслеживание активов"
    )

async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[
        InlineKeyboardButton("BTC", callback_data='check_BTC'),
        InlineKeyboardButton("ETH", callback_data='check_ETH'),
        InlineKeyboardButton("SOL", callback_data='check_SOL')
    ]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Выбери монету для анализа:", reply_markup=reply_markup)

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    coin = query.data.replace("check_", "").upper()
    symbol = f"{coin}USDT"
    analysis = get_analysis(symbol)
    text = (
        f"📊 {symbol}\n\n"
        f"• RSI: {analysis['rsi']}\n"
        f"• Цена: ${analysis['price']}\n"
        f"• Нижняя граница Bollinger: ${analysis['lower_band']}\n"
        f"• Объём: {analysis['volume_change']}% к среднему\n"
    )
    df = get_klines(symbol)
    df['RSI'] = compute_rsi(df['close'])
    chart_path = make_chart(df, symbol)
    with open(chart_path, "rb") as chart:
        await query.message.reply_photo(photo=InputFile(chart), caption=text)

# Background auto-analysis logic
def run_auto_analysis():
    symbols = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "AVAXUSDT", "MATICUSDT", "LINKUSDT", "ARBUSDT"]
    print("🔁 Автоанализ запущен")
    for symbol in symbols:
        try:
            result = get_analysis(symbol)
            print(f"[{symbol}] RSI: {result['rsi']}, Цена: {result['price']}, Объём: {result['volume_change']}%")
            if result['rsi'] < 30 and result['volume_change'] > 20:
                print(f"📢 Сигнал на покупку: {symbol}")
        except Exception as e:
            print(f"Ошибка анализа {symbol}: {e}")

def schedule_thread():
    schedule.every(15).minutes.do(run_auto_analysis)
    print("⏱️ Планировщик автоанализа активен...")
    while True:
        schedule.run_pending()
        time.sleep(5)

# Запуск Telegram и анализа параллельно
if __name__ == "__main__":
    threading.Thread(target=schedule_thread, daemon=True).start()
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("check", check))
    app.add_handler(CallbackQueryHandler(handle_callback))
    print("🤖 Бот запущен")

WEBHOOK_PATH = f"/{BOT_TOKEN}"
WEBHOOK_URL = f"https://{os.getenv('RAILWAY_STATIC_URL')}{WEBHOOK_PATH}"

app.run_webhook(
    listen="0.0.0.0",
    port=int(os.getenv('PORT', 8080)),
    webhook_path=WEBHOOK_PATH,
    webhook_url=WEBHOOK_URL
)


async def error_handler(update, context):
    logging.error(f"❌ Telegram error: {context.error}")
