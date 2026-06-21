from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

TOKEN = "8747579183:AAGEdi5ramP3XZ0EEzAQVOCB4IRnqvm8ANc"

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

    if step == "name":
        users[user_id]["name"] = text
        users[user_id]["step"] = "age"

        await update.message.reply_text(
            f"Приятно познакомиться, {text}!\n\n"
            "Сколько тебе лет?"
        )

    elif step == "age":
        users[user_id]["age"] = text
        users[user_id]["step"] = "goal"

        await update.message.reply_text(
            "Какая твоя главная цель?"
        )

    elif step == "goal":
        users[user_id]["goal"] = text
        users[user_id]["step"] = "time"

        await update.message.reply_text(
            "Через сколько времени ты хочешь достичь этой цели?"
        )

    elif step == "time":
        users[user_id]["time"] = text
        users[user_id]["step"] = "obstacle"

        await update.message.reply_text(
            "Что сейчас мешает тебе больше всего?"
        )

    elif step == "obstacle":
        users[user_id]["obstacle"] = text
        users[user_id]["step"] = "hours"

        await update.message.reply_text(
            "Сколько часов в день ты готов уделять развитию?"
        )

    elif step == "hours":
        users[user_id]["hours"] = text

        name = users[user_id]["name"]
        age = users[user_id]["age"]
        goal = users[user_id]["goal"]
        time_goal = users[user_id]["time"]
        obstacle = users[user_id]["obstacle"]
        hours = users[user_id]["hours"]

        await update.message.reply_text(
            f"📊 Твой профиль:\n\n"
            f"👤 Имя: {name}\n"
            f"🎂 Возраст: {age}\n"
            f"🎯 Цель: {goal}\n"
            f"⏳ Срок: {time_goal}\n"
            f"⚠️ Главное препятствие: {obstacle}\n"
            f"🕒 Время на развитие: {hours}\n\n"
            f"🚀 Отлично. Теперь я буду помогать тебе двигаться к цели."
        )

        users[user_id]["step"] = "done"


app = Application.builder().token(TOKEN).build()
async def plan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.chat_id

    if user_id not in users or "goal" not in users[user_id]:
        await update.message.reply_text(
            "Сначала пройди знакомство через /start"
        )
        return

    goal = users[user_id]["goal"]

    await update.message.reply_text(
        f"🎯 Твоя цель: {goal}\n\n"
        "📌 План на сегодня:\n\n"
        "1. Сделай одно действие, которое приблизит тебя к цели.\n"
        "2. Изучи что-то новое по своей теме.\n"
        "3. Запиши 3 идеи для улучшения своей жизни или проекта.\n\n"
        "🚀 Главное — не стоять на месте."
    )

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("план", plan))
app.add_handler(
    MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
)

print("ATLAS запущен")
app.run_polling()