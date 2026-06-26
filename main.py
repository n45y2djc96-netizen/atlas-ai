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

from payments import activate_pro, is_pro

TOKEN = "8747579183:AAE0h-I-GKJvard3F4YDWKuTWR0CPqbvyYc"
DATA_FILE = "users.json"

# ---------- LOAD ----------
def load_users():
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
    except:
        pass
    return {}

def save_users():
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(users, f, ensure_ascii=False, indent=2)
    except:
        pass

users = load_users()


# ---------- AI ----------
def ai_engine(user_text, user):
    text = user_text.lower()
    goal = user.get("goal", "неизвестна")

    if "заработ" in text:
        return f"💰 Твоя цель: {goal}\nНачни с навыка + практики"

    if "лен" in text:
        return "⚡ Сделай 1 маленький шаг прямо сейчас"

    if "что делать" in text:
        return "📌 Выбери 1 задачу и сделай её"

    if "мотивация" in text:
        return f"🔥 Ты ближе к цели: {goal}"

    return f"🤖 Понял тебя. Цель: {goal}"


# ---------- START ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_chat.id)

    users[user_id] = {
        "step": "name",
        "memory": [],
        "level": "beginner",
        "goal": "",
        "age": "",
        "time": ""
    }

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

    user = users[user_id]

    # memory FIX
    if "memory" not in user:
        user["memory"] = []

    user["memory"].append(text)
    user["memory"] = user["memory"][-20:]

    step = user["step"]

    if step == "name":
        user["name"] = text
        user["step"] = "age"
        save_users()
        await update.message.reply_text("Сколько тебе лет?")
        return

    elif step == "age":
        user["age"] = text
        user["step"] = "goal"
        save_users()
        await update.message.reply_text("Какая твоя цель?")
        return

    elif step == "goal":
        user["goal"] = text
        user["step"] = "time"
        save_users()
        await update.message.reply_text("За сколько времени?")
        return

    elif step == "time":
        user["time"] = text
        user["step"] = "done"
        save_users()

        await update.message.reply_text(
            f"📋 ГОТОВО:\n\n"
            f"👤 {user.get('name')}\n"
            f"🎯 {user.get('goal')}\n"
            f"⏳ {user.get('time')}\n\n"
            "🚀 Пиши мне что хочешь"
        )
        return

    # AI MODE
    answer = ai_engine(text, user)
    save_users()

    await update.message.reply_text(answer)


# ---------- PROFILE ----------
async def profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_chat.id)

    if user_id not in users:
        await update.message.reply_text("Сначала /start")
        return

    u = users[user_id]

    await update.message.reply_text(
        f"📊 ПРОФИЛЬ:\n\n"
        f"👤 {u.get('name')}\n"
        f"🎯 {u.get('goal')}\n"
        f"⏳ {u.get('time')}\n"
        f"🧠 {u.get('level')}"
    )


# ---------- PLAN ----------
async def plan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_chat.id)

    if user_id not in users:
        await update.message.reply_text("Сначала /start")
        return

    goal = users[user_id].get("goal", "цель")

    await update.message.reply_text(
        f"🎯 ЦЕЛЬ: {goal}\n\n"
        "1. 1 действие\n"
        "2. 30 минут работы\n"
        "3. Практика"
    )


# ---------- MOTIVATION ----------
async def motivation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_chat.id)

    if user_id not in users:
        await update.message.reply_text(
            "Сначала используй /start"
        )
        return

    name = users[user_id].get("name", "друг")
    goal = users[user_id].get("goal", "своей цели")

    await update.message.reply_text(
        f"🔥 {name}, помни:\n\n"
        f"Каждый день приближает тебя к цели:\n"
        f"🎯 {goal}\n\n"
        "Не жди идеального момента.\n"
        "Сделай хотя бы один шаг сегодня.\n\n"
        "🚀 Маленькие действия создают большие результаты!"
    )


# ---------- APP ----------
app = Application.builder().token(TOKEN).build()

async def upgrade(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_chat.id)

    if user_id not in users:
        await update.message.reply_text("Сначала используй /start")
        return

    users[user_id]["plan"] = "pro"
    save_users()

    await update.message.reply_text(
        "💎 Поздравляю! PRO режим активирован."
    )

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("profile", profile))
app.add_handler(CommandHandler("plan", plan))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message))
app.add_handler(CommandHandler("upgrade", upgrade))
app.add_handler(CommandHandler("motivation", motivation))

print("🚀 ATLAS RUNNING")
app.run_polling()