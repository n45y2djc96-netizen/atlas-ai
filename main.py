from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

TOKEN = "8747579183:AAGEdi5ramP3XZ0EEzAQVOCB4IRnqvm8ANc"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Привет!\n\n"
        "Я ATLAS — твой AI-стратег.\n\n"
        "Напиши мне свою главную цель."
    )


async def plan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📌 План на сегодня:\n\n"
        "1. Изучи что-нибудь новое 30 минут.\n"
        "2. Сделай одно действие для своей цели.\n"
        "3. Запиши 3 новые идеи.\n\n"
        "🚀 Двигайся вперёд каждый день."
    )


async def message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    await update.message.reply_text(
        f"Ты написал:\n\n{text}\n\n"
        "🔥 Интересно. Расскажи подробнее."
    )


app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("plan", plan))

app.add_handler(
    MessageHandler(filters.TEXT & ~filters.COMMAND, message)
)

print("ATLAS запущен")
app.run_polling()