import os
import asyncio
import nest_asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from signals import generate_signal

BOT_TOKEN = os.getenv("BOT_TOKEN")
chat_ids = set()
last_signals = {}  # ключ: (chat_id, symbol), значение: последняя рекомендация (action)
top_symbols = ["BTC", "ETH", "SOL", "DOGE", "TRX", "ADA", "SUI", "SHIB", "TON", "DOT", "PEPE"]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    chat_ids.add(chat_id)

    keyboard = [
        [InlineKeyboardButton(symbol, callback_data=symbol)] for symbol in top_symbols
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Привет! Я Крипто Scout 🌐\nВыбери монету для анализа:",
        reply_markup=reply_markup
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    chat_ids.add(chat_id)

    query = update.callback_query
    await query.answer()
    symbol = query.data

    signal_text, chart, action = await generate_signal(symbol)

    await query.edit_message_media(
        media=InputMediaPhoto(media=chart, caption=signal_text)
    )

    last_signals[(chat_id, symbol)] = action  # обновляем рекомендацию

async def periodic_notify(app):
    while True:
        for chat_id in chat_ids:
            for symbol in top_symbols:
                text, chart, action = await generate_signal(symbol)
                if last_signals.get((chat_id, symbol)) != action:
                    await app.bot.send_photo(chat_id=chat_id, photo=chart, caption=text)
                    last_signals[(chat_id, symbol)] = action
        await asyncio.sleep(60)

async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    asyncio.create_task(periodic_notify(app))

    print("🤖 Бот запущен!")
    await app.run_polling()

if __name__ == "__main__":
    nest_asyncio.apply()
    asyncio.run(main())
