import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, ContextTypes,
    CallbackQueryHandler
)
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

BOT_TOKEN = os.getenv("BOT_TOKEN")

# Обработка /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я Krypto Scout 🤖\nКаждые 15 минут я сканирую рынок.\nКоманды:\n/check — ручной анализ\n/track — отслеживание активов"
    )

# Обработка /check
async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("BTC", callback_data="BTC")],
        [InlineKeyboardButton("ETH", callback_data="ETH")],
        [InlineKeyboardButton("SOL", callback_data="SOL")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Выбери монету для анализа:", reply_markup=reply_markup)

# Обработка нажатий кнопок
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    symbol = query.data
    await query.edit_message_text(text=f"📊 Анализирую {symbol}...")

# Уведомление об ошибках
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    print(f"❌ Ошибка: {context.error}")

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("check", check))
    app.add_handler(CommandHandler("track", start))  # пока заглушка
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_error_handler(error_handler)

    print("🤖 Бот запущен")
    app.run_webhook(
        listen="0.0.0.0",
        webhook_path=int(os.getenv("PORT", 8000)),
        path="/"
    )