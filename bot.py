from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я Krypto Scout 🤖\nНапиши /проверка для сигнала.")

async def test_signal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔍 Проверка сигнала…")
    await update.message.reply_text(
        "🟢 Сигнал на покупку: BTC/USDT\n"
        "\n• RSI: 28 (растёт)"
        "\n• Цена: $61,200 (поддержка: $61,000)"
        "\n• Объём: +35%"
        "\n🎯 Цель: $63,500"
        "\n\n(пример сигнала)"
    )

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("проверка", test_signal))
    print("Bot started")
    app.run_polling()
