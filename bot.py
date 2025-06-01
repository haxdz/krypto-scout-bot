import os
import aiohttp
import asyncio
import nest_asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from signals import generate_signal

BOT_TOKEN = os.getenv("BOT_TOKEN")
chat_ids = set()
last_signals = {}  # ключ: (chat_id, symbol), значение: последний отправленный сигнал
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

    signal_text, chart = await generate_signal(symbol)
    await context.bot.send_photo(chat_id=chat_id, photo=chart, caption=signal_text)
    await query.edit_message_text(text=f"📊 Сигнал по {symbol}:\n{signal_text}")

    # Обновляем последний сигнал
    last_signals[(chat_id, symbol)] = signal_text

async def periodic_notify(app):
    while True:
        for chat_id in chat_ids:
            for symbol in top_symbols:
                text, chart = await generate_signal(symbol)
                # Сравниваем с последним сигналом
                if last_signals.get((chat_id, symbol)) != text:
                    await app.bot.send_photo(chat_id=chat_id, photo=chart, caption=text)
                    last_signals[(chat_id, symbol)] = text  # обновляем последний сигнал
        await asyncio.sleep(60)  # проверяем раз в минуту

async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    # Запускаем уведомления
    asyncio.create_task(periodic_notify(app))

    print("🤖 Бот запущен!")
    await app.run_polling()

if __name__ == "__main__":
    nest_asyncio.apply()
    asyncio.run(main())
