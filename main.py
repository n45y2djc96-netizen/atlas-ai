from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

TOKEN = "8747579183:AAE0h-I-GKJvard3F4YDWKuTWR0CPqbvyYc"

users = {}


# /start (полный диалог)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_chat.id

    users[user_id] = {"step": "name"}

    await update.message.reply_text(
        "👋 Привет! Я ATLAS — твой AI-ассистент.\n\n"
        "Как тебя зовут?"
    )


# основной обработчик
async def message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_chat.id
    text = update.message.text

    if user_id not in users:
        await update.message.reply_text("Нажми /start")
        return

    step = users[user_id]["step"]

    # ИМЯ
    if step == "name":
        users[user_id]["name"] = text
        users[user_id]["step"] = "age"

        await update.message.reply_text(
            f"Приятно познакомиться, {text} 👋\n\nСколько тебе лет?"
        )
        return

    # ВОЗРАСТ
    elif step == "age":
        users[user_id]["age"] = text
        users[user_id]["step"] = "goal"

        await update.message.reply_text(
            "🎯 Какая у тебя главная цель?"
        )
        return

    # ЦЕЛЬ
    elif step == "goal":
        users[user_id]["goal"] = text
        users[user_id]["step"] = "time"

        await update.message.reply_text(
            "⏳ За сколько времени хочешь достичь цели?"
        )
        return

    # СРОК
    elif step == "time":
        users[user_id]["time"] = text
        users[user_id]["step"] = "done"

        u = users[user_id]

        await update.message.reply_text(
            f"📋 Отлично! Я запомнил тебя:\n\n"
            f"👤 {u['name']}\n"
            f"🎂 {u['age']}\n"
            f"🎯 {u['goal']}\n"
            f"⏳ {u['time']}\n\n"
            "🚀 Теперь используй /plan или /profile"
        )
        return


# PROFILE
async def profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_chat.id

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


# PLAN
async def plan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_chat.id

    if user_id not in users:
        await update.message.reply_text("Сначала /start")
        return

    goal = users[user_id].get("goal", "твоя цель")

    await update.message.reply_text(
        f"🎯 ЦЕЛЬ: {goal}\n\n"
        "📌 ПЛАН НА ДЕНЬ:\n"
        "1. Сделай 1 важный шаг\n"
        "2. Учись 30 минут\n"
        "3. Запиши идеи\n\n"
        "🚀 Главное — действие"
    )


# MOTIVATION
async def motivation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_chat.id

    if user_id not in users:
        await update.message.reply_text("Сначала /start")
        return

    name = users[user_id].get("name", "друг")
    goal = users[user_id].get("goal", "цели")

    await update.message.reply_text(
        f"🔥 {name}, помни:\n\n"
        f"Ты идёшь к: {goal}\n\n"
        "Каждый день — это шаг вперёд.\n"
        "Не останавливайся 🚀"
    )


# SMART PLAN
async def smart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_chat.id

    if user_id not in users:
        await update.message.reply_text("Сначала /start")
        return

    goal = users[user_id].get("goal", "").lower()

    if "бизнес" in goal or "деньги" in goal:
        text = "💰 Бизнес:\n1. Идея\n2. Анализ\n3. Первый продукт\n4. Клиенты"
    elif "спорт" in goal:
        text = "🏋️ Спорт:\n1. Тренировка\n2. Питание\n3. Сон\n4. Дисциплина"
    else:
        text = "📈 Развитие:\n1. Учись\n2. Практикуй\n3. Действуй"

    await update.message.reply_text(text)


# APP
app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("profile", profile))
app.add_handler(CommandHandler("plan", plan))
app.add_handler(CommandHandler("motivation", motivation))
app.add_handler(CommandHandler("smart", smart))

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message))

print("ATLAS запущен 🚀")
app.run_polling()