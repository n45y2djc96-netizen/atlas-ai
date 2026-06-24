import json
import os
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

TOKEN = "8747579183:AAE0h-I-GKJvard3F4YDWKuTWR0CPqbvyYc"
DATA_FILE = "users.json"

# ---------- LOAD ----------
def load_users():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_users():
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)

users = load_users()


# ---------- START ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_chat.id)

    users[user_id] = {"step": "name"}
    save_users()

    await update.message.reply_text(
        "👋 Привет! Я ATLAS\n\nКак тебя зовут?"
    )


# ---------- MESSAGE ----------
async def message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_chat.id)
    text = update.message.text

    if user_id not in users:
        await update.message.reply_text("Нажми /start")
        return

    step = users[user_id]["step"]

    if step == "name":
        users[user_id]["name"] = text
        users[user_id]["step"] = "age"
        save_users()

        await update.message.reply_text("Сколько тебе лет?")
        return

    elif step == "age":
        users[user_id]["age"] = text
        users[user_id]["step"] = "goal"
        save_users()

        await update.message.reply_text("Какая цель?")
        return

    elif step == "goal":
        users[user_id]["goal"] = text
        users[user_id]["step"] = "time"
        save_users()

        await update.message.reply_text("За сколько времени?")
        return

    elif step == "time":
        users[user_id]["time"] = text
        users[user_id]["step"] = "done"
        save_users()

        u = users[user_id]

        await update.message.reply_text(
            f"📋 Готово!\n\n"
            f"👤 {u['name']}\n"
            f"🎯 {u['goal']}\n"
            f"⏳ {u['time']}"
        )
        return


# ---------- PLAN ----------
async def plan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_chat.id)

    if user_id not in users:
        await update.message.reply_text("Сначала /start")
        return

    goal = users[user_id].get("goal", "цель")

    await update.message.reply_text(
        f"🎯 Цель: {goal}\n\n"
        "1. Действие\n2. Обучение\n3. Практика"
    )


# ---------- APP ----------
app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("plan", plan))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message))

print("BOT STARTED")

app.run_polling()