from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

TOKEN = "8747579183:AAE0h-I-GKJvard3F4YDWKuTWR0CPqbvyYc"

# Хранилище данных пользователей
users = {}


# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_chat.id

    users[user_id] = {"step": "name"}

    await update.message.reply_text(
        "👋 Привет!\n\n"
        "Я ATLAS — твой AI-стратег.\n\n"
        "Как тебя зовут?"
    )


# Обработка сообщений
async def message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_chat.id
    text = update.message.text

    if user_id not in users:
        await update.message.reply_text(
            "Напиши /start чтобы начать."
        )
        return

    step = users[user_id]["step"]

    # Имя
    if step == "name":
        users[user_id]["name"] = text
        users[user_id]["step"] = "age"

        await update.message.reply_text(
            "Сколько тебе лет?"
        )
        return

    # Возраст
    elif step == "age":
        users[user_id]["age"] = text
        users[user_id]["step"] = "goal"

        await update.message.reply_text(
            "Какая у тебя главная цель?"
        )
        return

    # Цель
    elif step == "goal":
        users[user_id]["goal"] = text
        users[user_id]["step"] = "time"

        await update.message.reply_text(
            "За сколько времени ты хочешь достичь этой цели?"
        )
        return

    # Срок
    elif step == "time":
        users[user_id]["time"] = text
        users[user_id]["step"] = "done"

        name = users[user_id]["name"]
        age = users[user_id]["age"]
        goal = users[user_id]["goal"]
        time_goal = users[user_id]["time"]

        await update.message.reply_text(
            f"📋 Твоя анкета:\n\n"
            f"👤 Имя: {name}\n"
            f"🎂 Возраст: {age}\n"
            f"🎯 Цель: {goal}\n"
            f"⏳ Срок достижения: {time_goal}\n\n"
            "🔥 Отлично! Я всё запомнил."
        )
        return

    # Изменение цели
    elif step == "new_goal":
        users[user_id]["goal"] = text
        users[user_id]["step"] = "done"

        await update.message.reply_text(
            f"✅ Новая цель сохранена:\n\n🎯 {text}"
        )
        return

    # После заполнения анкеты
    else:
        await update.message.reply_text(
            "Я уже сохранил твою анкету.\n\n"
            "Доступные команды:\n"
            "/profile - профиль\n"
            "/plan - план на день\n"
            "/motivation - мотивация\n"
            "/change_goal - изменить цель"
        )


# Команда /profile
async def profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_chat.id

    if user_id not in users:
        await update.message.reply_text(
            "Сначала пройди регистрацию через /start"
        )
        return

    user = users[user_id]

    await update.message.reply_text(
        f"📋 Твой профиль:\n\n"
        f"👤 Имя: {user.get('name', 'Не указано')}\n"
        f"🎂 Возраст: {user.get('age', 'Не указано')}\n"
        f"🎯 Цель: {user.get('goal', 'Не указано')}\n"
        f"⏳ Срок: {user.get('time', 'Не указано')}"
    )


# Команда /plan
async def plan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_chat.id

    if user_id not in users:
        await update.message.reply_text(
            "Сначала пройди регистрацию через /start"
        )
        return

    goal = users[user_id].get("goal", "твоя цель")

    await update.message.reply_text(
        f"🎯 Твоя цель: {goal}\n\n"
        "📌 План на сегодня:\n\n"
        "1️⃣ Сделай одно действие для достижения цели.\n"
        "2️⃣ Изучи что-то новое 30 минут.\n"
        "3️⃣ Запиши 3 идеи для развития.\n"
        "4️⃣ Проанализируй свой день.\n\n"
        "🚀 Главное — двигаться вперёд каждый день."
    )


# Команда /motivation
async def motivation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_chat.id

    if user_id not in users:
        await update.message.reply_text(
            "Сначала пройди регистрацию через /start"
        )
        return

    name = users[user_id].get("name", "друг")
    goal = users[user_id].get("goal", "своей цели")

    await update.message.reply_text(
        f"🔥 {name}, помни:\n\n"
        f"Твоя цель:\n🎯 {goal}\n\n"
        "Каждый день делай хотя бы один шаг вперёд.\n\n"
        "🚀 Маленькие действия приводят к большим результатам."
    )


# Команда /change_goal
async def change_goal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_chat.id

    if user_id not in users:
        await update.message.reply_text(
            "Сначала пройди регистрацию через /start"
        )
        return

    users[user_id]["step"] = "new_goal"

    await update.message.reply_text(
        "🎯 Напиши свою новую цель."
    )


# Создание приложения
app = Application.builder().token(TOKEN).build()

# Команды
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("profile", profile))
app.add_handler(CommandHandler("plan", plan))
app.add_handler(CommandHandler("motivation", motivation))
app.add_handler(CommandHandler("change_goal", change_goal))

# Сообщения
app.add_handler(
    MessageHandler(filters.TEXT & ~filters.COMMAND, message)
)

print("ATLAS запущен")
app.run_polling()