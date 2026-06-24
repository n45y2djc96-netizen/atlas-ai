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


# загрузка данных из файла
def load_users():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


# сохранение данных в файл
def save_users():
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)


users = load_users()


# START
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_chat.id)

    users[user_id] = {"step": "name"}
    save_users()

    await update.message.reply_text(
        "👋 Привет!\n\nКак тебя зовут?"
    )


# MESSAGE FLOW
async def message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_chat.id)
    text = update.message.text

    if user_id not in users:
        await update.message.reply_text("Напиши /start")
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

        await update.message.reply_text("Какая твоя цель?")
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

        await update.message.reply_text(
            f"📋 Готово!\n\n"
            f"👤 {users[user_id]['name']}\n"
            f"🎯 {users[user_id]['goal']}\n"
            f"⏳ {users[user_id]['time']}"
        )
        return


# PROFILE
async def profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_chat.id)

    if user_id not in users:
        await update.message.reply_text("Сначала /start")
        return

    u = users[user_id]

    await update.message.reply_text(
        f"📋 Профиль:\n\n"
        f"👤 {u.get('name')}\n"
        f"🎂 {u.get('age')}\n"
        f"🎯 {u.get('goal')}\n"
        f"⏳ {u.get('time')}"
    )


# APP
app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("profile", profile))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message))

print("BOT STARTED")
app.run_polling()