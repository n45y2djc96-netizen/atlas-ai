from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

TOKEN = "8747579183:AAGEdi5ramP3XZ0EEzAQVOCB4IRnqvm8ANc"

# Хранилище данных пользователей (пока временное)
users = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.chat_id

    users[user_id] = {"step": "name"}

    await update.message.reply_text(
        "👋 Привет!\n\n"
        "Я ATLAS — твой личный AI-стратег.\n\n"
        "Для начала скажи, как тебя зовут?"
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.chat_id
    text = update.message.text

    if user_id not in users:
        await update.message.reply_text(
            "Напиши /start чтобы начать."
        )
        return

    step = users[user_id]["step"]

    # Получаем имя
    if step == "name":
        users[user_id]["name"] = text
        users[user_id]["step"] = "age"

        await update.message.reply_text(
            f"Приятно познакомиться, {text}.\n\n"
            "Сколько тебе лет?"
        )

    # Получаем возраст
    elif step == "age":
        users[user_id]["age"] = text
        users[user_id]["step"] = "goal"

        await update.message.reply_text(
            "Какая твоя главная цель?"
        )

    # Получаем цель
    elif step == "goal":
        users[user_id]["goal"] = text

        name = users[user_id]["name"]
        age = users[user_id]["age"]
        goal = users[user_id]["goal"]

        await update.message.reply_text(
            f"Спасибо, {name}.\n\n"
            f"Я запомнил:\n"
            f"Возраст: {age}\n"
            f"Главная цель: {goal}\n\n"
            "Теперь я буду помогать тебе двигаться к этой цели 🚀"
        )

        users[user_id]["step"] = "done"


app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("ATLAS запущен")
app.run_polling()