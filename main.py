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

def get_id(update: Update):
    return update.effective_chat.id


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = get_id(update)

    users[user_id] = {"step": "name"}

    await update.message.reply_text(
        "👋 Привет!\nЯ ATLAS.\nКак тебя зовут?"
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return

    user_id = get_id(update)
    text = update.message.text

    if user_id not in users:
        await update.message.reply_text("Напиши /start")
        return

    step = users[user_id]["step"]

    if step == "name":
        users[user_id]["name"] = text
        users[user_id]["step"] = "goal"

        await update.message.reply_text("Какая твоя цель?")

    elif step == "goal":
        users[user_id]["goal"] = text
        users[user_id]["step"] = "done"

        await update.message.reply_text(
            f"🔥 Принято!\nТвоя цель: {text}\n\nТеперь напиши /план"
        )


async def plan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = get_id(update)

    goal = users.get(user_id, {}).get("goal", "нет цели")

    await update.message.reply_text(
        f"🎯 Цель: {goal}\n\n"
        "📌 План:\n1. Действие\n2. Обучение\n3. Идеи"
    )


app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("план", plan))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("ATLAS запущен")
app.run_polling()