from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

TOKEN = "8747579183:AAGEdi5ramP3XZ0EEzAQVOCB4IRnqvm8ANc

# Здесь временно будут храниться данные пользователей
users = {}


# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_chat.id

    users[user_id] = {"step": "name"}

    await update.message.reply_text(
        "👋 Привет!\n\n"
        "Я ATLAS — твой личный AI-стратег.\n\n"
        "Для начала скажи, как тебя зовут?"
    )


# Обработка сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return

    user_id = update.effective_chat.id
    text = update.message.text

    if user_id not in users:
        await update.message.reply_text(
            "Напиши /start чтобы начать."
        )
        return

    step = users[user_id]["step"]

    # Имя
    if step == "name":
        users[user_id]["name"] = text
        users[user_id]["step"] = "goal"

        await update.message.reply_text(
            f"Приятно познакомиться, {text}!\n\n"
            "Какая твоя главная цель?"
        )

    # Цель
    elif step == "goal":
        users[user_id]["goal"] = text
        users[user_id]["step"] = "done"

        await update.message.reply_text(
            f"🔥 Отлично!\n\n"
            f"Твоя цель: {text}\n\n"
            f"Теперь используй команду /план"
        )


# Команда /план
async def plan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_chat.id

    if user_id not in users:
        await update.message.reply_text(
            "Сначала пройди знакомство через /start"
        )
        return

    goal = users[user_id].get("goal", "не указана")

    await update.message.reply_text(
        f"🎯 Твоя цель: {goal}\n\n"
        "📌 План на сегодня:\n\n"
        "1. Сделай одно действие, которое приблизит тебя к цели.\n"
        "2. Изучи что-то новое минимум 30 минут.\n"
        "3. Запиши 3 идеи для развития.\n\n"
        "🚀 Каждый день становись лучше."
    )


# Создание приложения
app = Application.builder().token(TOKEN).build()

# Команды
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("план", plan))

# Сообщения
app.add_handler(
    MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
)

print("ATLAS запущен")
app.run_polling()