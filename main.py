from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

TOKEN = "8747579183:AAGmfGAN4sq7X643y6DmdEUh1IJIgSRqxRA"


users = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_chat.id

    users[user_id] = {"step": "name"}

    await update.message.reply_text(
        "👋 Привет!\n\n"
        "Я ATLAS — твой AI-стратег.\n\n"
        "Как тебя зовут?"
    )


async def message(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
        users[user_id]["step"] = "age"

        await update.message.reply_text(
            "Сколько тебе лет?"
        )
        return

    # Возраст
    elif step == "age":
        users[user_id]["age"] = text
        users[user_id]["step"] = "goal"

        await update.message.reply_text(
            "Какая у тебя главная цель?"
        )
        return

    # Цель
    elif step == "goal":
        users[user_id]["goal"] = text
        users[user_id]["step"] = "time"

        await update.message.reply_text(
            "За сколько времени ты хочешь достичь этой цели?"
        )
        return

    # Срок достижения
    elif step == "time":
        users[user_id]["time"] = text
        users[user_id]["step"] = "done"

        name = users[user_id]["name"]
        age = users[user_id]["age"]
        goal = users[user_id]["goal"]
        time_goal = users[user_id]["time"]

        await update.message.reply_text(
            f"📋 Твоя анкета:\n\n"
            f"👤 Имя: {name}\n"
            f"🎂 Возраст: {age}\n"
            f"🎯 Цель: {goal}\n"
            f"⏳ Срок достижения: {time_goal}\n\n"
            f"🔥 Отлично! Я всё запомнил."
        )
        return

    else:
        await update.message.reply_text(
            "Я уже сохранил твою анкету. Скоро мы добавим новые функции 🚀"
        )


app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(
    MessageHandler(filters.TEXT & ~filters.COMMAND, message)
)

print("ATLAS запущен")
app.run_polling()