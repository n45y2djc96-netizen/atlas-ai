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
from motivation_texts import get_motivation
from ai import chat_ai
from search import search_web
from internet import need_internet
from memory import update_memory
from pro_keyboard import pro_keyboard
from telegram.ext import CallbackQueryHandler
import time
from datetime import timedelta
from limits import (
    init_user,
    check_reset,
    can_send,
    add_message
)
import asyncio
from scheduler import check_users
from pro import activate_pro, check_pro

TOKEN = "8747579183:AAGlnU03s7XUeFNVe3jqAgPH-UB1GiHcDJU"
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
        "facts": [],
        "level": "beginner",
        "goal": "",
        "age": "",
        "time": "",
        "name": "",
        "messages_today": 0,
        "reset_time": 0,
        "plan": "free",
    
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
    init_user(user)

    if check_reset(user):
        save_users()

        await update.message.reply_text(
            "🎉 Бесплатный доступ снова открыт!\n\n"
            "🚀 Можно продолжать пользоваться ATLAS."
        )
    
    now = int(time.time())

    if user.get("reset_time", 0) == 0:
        user["reset_time"] = now + 86400

    if now >= user["reset_time"]:
        user["messages_today"] = 0
        user["reset_time"] = now + 86400
        save_users()

        await update.message.reply_text(
            "🎉 Бесплатный доступ снова открыт!\n\n"
            "Рад видеть тебя снова ❤️\n\n"
            "🚀 Можешь продолжить пользоваться ATLAS."
        )
    
    if "facts" not in user:
        user["facts"] = []

    # memory FIX
    if "memory" not in user:
        user["memory"] = []

    user["memory"].append(text)
    user["memory"] = user["memory"][-20:]

    step = user["step"]
    if not can_send(user):
        await update.message.reply_text(
            "💎 Бесплатный лимит сообщений закончился.\n\n"
            "Следующий доступ откроется через 24 часа.",
            reply_markup=pro_keyboard()
        )
        return
    
    
    
    # ---------- BUTTONS ----------
    if text == "🎯 Цель":
        goal = user.get("goal", "Цель не указана")

        await update.message.reply_text(f"🎯 Твоя цель:\n\n{goal}")
        return

    if text == "📈 Прогресс":
        progress = user.get("progress", 0)

        await update.message.reply_text(f"📈 Выполнено шагов: {progress}")
        return

    if text == "🔥 Мотивация":
       await update.message.reply_text(
           get_motivation()
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
        await update.message.reply_text("💎 PRO скоро появится.\nСледи за обновлениями.")
        return

   
    
     # ---------- STEP LOGIC ----------
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




# ---------- AI (ИСПРАВЛЕНО ТУТ) ----------
    t = text.lower()

    if "меня зовут" in t:
        user["facts"].append(text)

    if "мне " in t and "лет" in t:
        user["facts"].append(text)

    if "я люблю" in t:
        user["facts"].append(text)

    if "моя цель" in t:
        user["facts"].append(text)

    user["facts"] = user["facts"][-30:]
    
    internet = None

    if need_internet(text):
        internet = search_web(text)

    if internet:
        text = f"""
    Вопрос пользователя:
    {text}

    Свежая информация:

    {internet}

    Используй только эту информацию при ответе.
    """
    
    update_memory(user, text)
    
    add_message(user)
    save_users()
    
    answer = chat_ai(text, user["memory"], user)

    await update.message.reply_text(answer)

    save_users()



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



# ---------- BUTTONS ----------
async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "buy_pro":
        await query.edit_message_text(
            "💎 Скоро здесь появится настоящая покупка PRO."
        )

    elif query.data == "remind_me":
        await query.edit_message_text(
            "✅ Отлично!\n\n"
            "Через 24 часа я снова напомню, что бесплатный доступ открыт."
        )

async def free_access_notification(context: ContextTypes.DEFAULT_TYPE):
    user_id = context.job.data

    if user_id not in users:
        return

    users[user_id]["messages_today"] = 0
    users[user_id]["reset_time"] = 0
    save_users()

    await context.bot.send_message(
        chat_id=user_id,
        text=
        "🎉 Бесплатный доступ снова открыт!\n\n"
        "ATLAS снова готов помочь.\n\n"
        "🚀 Можешь продолжить пользоваться ботом."
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
app.add_handler(CallbackQueryHandler(buttons))

print("🚀 ATLAS RUNNING")

async def post_init(application):
    asyncio.create_task(check_users(application.bot))

app.post_init = post_init

app.run_polling()