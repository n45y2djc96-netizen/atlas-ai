from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

TOKEN = "8747579183:AAGEdi5ramP3XZ0EEzAQVOCB4IRnqvm8ANc" 

# Здесь временно храним данные пользователей
users = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_chat.id

    users[user_id] = {"step": "level"}

    await update.message.reply_text(
        "👋 Привет!\n\n"
        "Я ATLAS — твой AI-стратег.\n\n"
        "Напиши свою главную цель."
    )


async def plan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_chat.id

    if user_id not in users or "goal" not in users[user_id]:
        await update.message.reply_text(
            "Сначала напиши свою цель через /start"
        )
        return

    goal = users[user_id]["goal"]

    await update.message.reply_text(
        f"🎯 Твоя цель: {goal}\n\n"
        "📌 План на сегодня:\n\n"
        "1. Сделай одно действие для достижения цели.\n"
        "2. Изучи что-то новое 30 минут.\n"
        "3. Запиши 3 идеи для развития.\n\n"
        "🚀 Каждый день двигайся вперёд."
    )


async def message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_chat.id
    text = update.message.text

    if user_id in users and users[user_id]["step"] == "level":
    users[user_id]["level"] = text
    users[user_id]["step"] = "goal"

    await update.message.reply_text(
        "Понял 👍\n\nТеперь напиши свою главную цель."
    )
    
    return

elif user_id in users and users[user_id]["step"] == "goal":
    users[user_id]["goal"] = text
    users[user_id]["step"] = "done"

    await update.message.reply_text(
        "🔥 Отлично!\n\nЯ запомнил твою цель.\nТеперь используй /plan"
    )

        await update.message.reply_text(
            f"🔥 Отлично!\n\n"
            f"Я сохранил твою цель:\n\n"
            f"🎯 {text}\n\n"
            f"Теперь используй команду /plan"
        )

    else:
        await update.message.reply_text(
            "Я запомнил твоё сообщение. Используй /plan для получения плана."
        )


app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("plan", plan))

app.add_handler(
    MessageHandler(filters.TEXT & ~filters.COMMAND, message)
)

print("ATLAS запущен")
app.run_polling()