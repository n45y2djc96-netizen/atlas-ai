from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = "8747579183:AAGEdi5ramP3XZ0EEzAQVOCB4IRnqvm8ANc"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Привет!\n\n"
        "Я ATLAS.\n"
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


app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("plan", plan))

print("ATLAS запущен")
app.run_polling()