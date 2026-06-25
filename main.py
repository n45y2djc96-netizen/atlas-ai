from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)
import asyncio

TOKEN = "8747579183:AAE0h-I-GKJvard3F4YDWKuTWR0CPqbvyYc"

users = {}

# ---------- START ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_chat.id)

    users[user_id] = {
        "step": "name",
        "plan": "free"
    }

    await update.message.reply_text(
        "👋 Привет! Я ATLAS\n\nКак тебя зовут?"
    )


# ---------- MESSAGE FLOW ----------
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
        await update.message.reply_text("Сколько тебе лет?")
        return

    elif step == "age":
        users[user_id]["age"] = text
        users[user_id]["step"] = "goal"
        await update.message.reply_text("Какая твоя цель?")
        return

    elif step == "goal":
        users[user_id]["goal"] = text
        users[user_id]["step"] = "time"
        await update.message.reply_text("За сколько времени?")
        return

    elif step == "time":
        users[user_id]["time"] = text
        users[user_id]["step"] = "done"

        u = users[user_id]

        await update.message.reply_text(
            f"📋 ГОТОВО:\n\n"
            f"👤 {u['name']}\n"
            f"🎯 {u['goal']}\n"
            f"⏳ {u['time']}\n\n"
            "🚀 Используй /plan /profile /upgrade"
        )
        return

    # 🤖 AI режим
    goal = users[user_id].get("goal", "цель")

    await update.message.reply_text(
        f"🤖 Я думаю...\n\n"
        f"Цель: {goal}\n\n"
        "👉 Делай 1 шаг каждый день"
    )


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
        f"💎 План: {u.get('plan','free')}"
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
        "3. Практика\n\n"
        "🚀 Действие > мысли"
    )


# ---------- UPGRADE ----------
async def upgrade(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_chat.id)

    if user_id not in users:
        await update.message.reply_text("Сначала /start")
        return

    users[user_id]["plan"] = "pro"

    await update.message.reply_text(
        "💎 PRO активирован!\n\n"
        "Теперь у тебя расширенные возможности 🚀"
    )


# ---------- AI MEMORY LOOP (опционально) ----------
async def reminder(app):
    while True:
        await asyncio.sleep(60 * 60 * 24)  # 1 день

        for user_id in users:
            try:
                goal = users[user_id].get("goal", "цель")

                await app.bot.send_message(
                    chat_id=user_id,
                    text=f"🔔 Напоминание:\nДвигайся к цели:\n🎯 {goal}"
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
app.add_handler(CommandHandler("upgrade", upgrade))

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message))

print("🚀 ATLAS FINAL RUNNING")
app.run_polling(on_startup=on_start)