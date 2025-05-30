import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from scheduler import scheduler
import asyncio
import nest_asyncio  # добавь это

BOT_TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("BTC", callback_data='BTC')],
        [InlineKeyboardButton("ETH", callback_data='ETH')],
        [InlineKeyboardButton("SOL", callback_data='SOL')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Привет! Я Крипто Scout 🌐\nВыбери монету для анализа:", reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    symbol = query.data
    signal = await generate_signal(symbol)
    await query.edit_message_text(text=f"📊 Сигнал по {symbol}:\n{signal}")

async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("check", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    # Планировщик
    scheduler.start()

    print("🤖 Бот запущен!")
    await app.run_polling()

if __name__ == "__main__":
    nest_asyncio.apply()  # важно!
    asyncio.run(main())
