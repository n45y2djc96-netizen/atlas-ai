import json
import os
import asyncio
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

# ---------- LOAD / SAVE ----------
def load_users():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_users():
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)

users = load_users()


# ---------- MEMORY ----------
def add_memory(user_id, text):
    if "memory" not in users[user_id]:
        users[user_id]["memory"] = {"history": []}

    users[user_id]["memory"]["history"].append(text)
    users[user_id]["memory"]["history"] = users[user_id]["memory"]["history"][-20:]


# ---------- AI (без OpenAI) ----------
def ai_response(text):
    t = text.lower()

    if "деньги" in t or "заработ" in t:
        return "💰 Начни с навыка: фриланс, услуги, контент или перепродажа"

    if "мотивация" in t:
        return "🔥 Ты либо делаешь шаг, либо стоишь на месте"

    if "что делать" in t:
        return "📌 Сделай 1 маленький шаг прямо сейчас"

    return "🤖 Я учусь. Попробуй задать вопрос проще"


# ---------- START ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_chat.id)

    users[user_id] = {"step": "name", "memory": {"history": []}}
    save_users()

    await update.message.reply_text(
        "👋 Привет! Я ATLAS — твой AI-ассистент\n\nКак тебя зовут?"
    )


# ---------- MESSAGE FLOW ----------
async def message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_chat.id)
    text = update.message.text

    if user_id not in users:
        await update.message.reply_text("Нажми /start")
        return

    add_memory(user_id, text)

    step = users[user_id]["step"]

    # NAME
    if step == "name":
        users[user_id]["name"] = text
        users[user_id]["step"] = "age"
        save_users()

        await update.message.reply_text("Сколько тебе лет?")
        return

    # AGE
    elif step == "age":
        users[user_id]["age"] = text
        users[user_id]["step"] = "goal"
        save_users()

        await update.message.reply_text("Какая твоя цель?")
        return

    # GOAL
    elif step == "goal":
        users[user_id]["goal"] = text
        users[user_id]["step"] = "time"
        save_users()

        await update.message.reply_text("За сколько времени?")
        return

    # TIME
    elif step == "time":
        users[user_id]["time"] = text
        users[user_id]["step"] = "done"
        save_users()

        await update.message.reply_text(
            f"📋 ГОТОВО:\n\n"
            f"👤 {users[user_id]['name']}\n"
            f"🎯 {users[user_id]['goal']}\n"
            f"⏳ {users[user_id]['time']}\n\n"
            "🚀 Используй /plan /profile /smart"
        )
        return

    # AI MODE
    else:
        await update.message.reply_text(ai_response(text))


# ---------- PROFILE ----------
async def profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_chat.id)

    if user_id not in users:
        await update.message.reply_text("Сначала /start")
        return

    u = users[user_id]

    await update.message.reply_text(
        f"📋 ПРОФИЛЬ:\n\n"
        f"👤 {u.get('name')}\n"
        f"🎂 {u.get('age')}\n"
        f"🎯 {u.get('goal')}\n"
        f"⏳ {u.get('time')}"
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
        "📌 ПЛАН:\n"
        "1. 1 действие\n"
        "2. 30 мин обучения\n"
        "3. Практика\n\n"
        "🚀 Делай каждый день"
    )


# ---------- SMART ----------
async def smart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_chat.id)

    if user_id not in users:
        await update.message.reply_text("Сначала /start")
        return

    goal = users[user_id].get("goal", "").lower()

    if "бизнес" in goal:
        text = "💼 Бизнес:\n1. Идея\n2. Проверка\n3. Клиенты"
    elif "спорт" in goal:
        text = "🏋️ Спорт:\n1. Тренировка\n2. Питание\n3. Сон"
    else:
        text = "📈 Развитие:\n1. Учись\n2. Делай\n3. Улучшай"

    await update.message.reply_text(text)


# ---------- REMINDER ----------
async def reminder(app):
    while True:
        await asyncio.sleep(60 * 60 * 24)

        for user_id in users:
            try:
                await app.bot.send_message(
                    chat_id=user_id,
                    text="⏰ Напоминание: сделай 1 шаг к цели сегодня"
                )
            except:
                pass


async def on_start(app):
    asyncio.create_task(reminder(app))


# ---------- APP ----------
app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("profile", profile))
app.add_handler(CommandHandler("plan", plan))
app.add_handler(CommandHandler("smart", smart))

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message))

print("🚀 ATLAS FULL STARTED")
app.run_polling(on_startup=on_start)