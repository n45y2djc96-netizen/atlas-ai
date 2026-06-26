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
from goals import change_goal, get_goal
from progress import add_progress, get_progress
from reminders import get_reminder
from atlas_keyboard import main_keyboard

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
    "👋 Привет! Я ATLAS\n\nКак тебя зовут?",
    reply_markup=main_keyboard()
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
    
# ---------- BUTTONS ----------
if text == "🎯 Цель":
    goal = user.get("goal", "Цель не указана")

    await update.message.reply_text(
        f"🎯 Твоя цель:\n\n{goal}"
    )
    return

if text == "📈 Прогресс":
    progress = user.get("progress", 0)

    await update.message.reply_text(
        f"📈 Выполнено шагов: {progress}"
    )
    return

if text == "🔥 Мотивация":
    await update.message.reply_text(
        "🔥 Никогда не сдавайся. Один шаг каждый день меняет жизнь."
    )
    return

if text == "📋 План":
    goal = user.get("goal", "цель")

    await update.message.reply_text(
        f"📋 План для цели:\n🎯 {goal}\n\n"
        "1. Сделай одно действие.\n"
        "2. Изучи что-то новое.\n"
        "3. Зафиксируй результат."
    )
    return

if text == "💎 PRO":
    await update.message.reply_text(
        "💎 PRO скоро появится.\nСледи за обновлениями."
    )
    return
    
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


# ---------- GOAL ----------
async def goal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_chat.id)

    if user_id not in users:
        await update.message.reply_text("Сначала используй /start")
        return

    goal_text = get_goal(users, user_id)

    await update.message.reply_text(
        f"🎯 Твоя цель:\n\n{goal_text}"
    )


# ---------- PROGRESS ----------
async def progress(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_chat.id)

    if user_id not in users:
        await update.message.reply_text("Сначала используй /start")
        return

    total = get_progress(users, user_id)

    await update.message.reply_text(
        f"📈 Твой прогресс:\n\n🔥 Выполнено шагов: {total}"
    )


# ---------- DONE ----------
async def done(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_chat.id)

    result = add_progress(users, user_id)
    save_users()

    await update.message.reply_text(result)


# ---------- REMIND ----------
async def remind(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        get_reminder()
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
app.add_handler(CommandHandler("goal", goal))
app.add_handler(CommandHandler("progress", progress))
app.add_handler(CommandHandler("done", done))
app.add_handler(CommandHandler("remind", remind))

print("🚀 ATLAS RUNNING")
app.run_polling()