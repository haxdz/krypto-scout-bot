import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from scheduler import start_scheduler
from signals import generate_signal
import asyncio
import nest_asyncio

BOT_TOKEN = os.getenv("BOT_TOKEN")
chat_ids = set()  # Запоминаем всех пользователей для уведомлений

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_ids.add(update.effective_chat.id)
    start_scheduler(context.application, update.effective_chat.id)  # Запускаем уведомления для каждого нового чата
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
    signal_text, chart = await generate_signal(symbol)
    await context.bot.send_photo(chat_id=update.effective_chat.id, photo=chart, caption=signal_text)
    await query.edit_message_text(text=f"📊 Сигнал по {symbol}:\n{signal_text}")

async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("🤖 Бот запущен!")
    await app.run_polling()

if __name__ == "__main__":
    nest_asyncio.apply()
    asyncio.run(main())
