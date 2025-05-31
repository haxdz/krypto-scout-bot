from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from scheduler import scheduler
from signals import generate_signal  # Вот здесь добавляем
import asyncio
import nest_asyncio

nest_asyncio.apply()
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
    # Вызываем функцию генерации сигнала
    text_signal, chart = await generate_signal(symbol)
    await query.edit_message_text(text=text_signal)
    # Отправляем график как фото
    await query.message.reply_photo(photo=chart)


async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    scheduler.start()  # без await
    await app.run_polling()


if __name__ == "__main__":
    asyncio.run(main())
