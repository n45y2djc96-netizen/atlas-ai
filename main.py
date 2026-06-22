from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = "8747579183:AAGEdi5ramP3XZ0EEzAQVOCB4IRnqvm8ANc"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я работаю!")

app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))

print("ATLAS запущен")
app.run_polling()