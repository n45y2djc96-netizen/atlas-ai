import json
import os
from telegram import Update, SuccessfulPayment
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    PreCheckoutQueryHandler,
    ContextTypes,
    filters
)

from payments import is_pro
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
from stars import buy_pro
from memory import update_memory
from atlas_memory import analyze_user

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

    if user_id not in users:
        users[user_id] = {
            "step": "name",

            "name": "",
            "age": "",
            "goal": "",
            "time": "",

            "level": "beginner",

            "memory": [],
            "facts": [],

            # Память ATLAS X
            "dreams": [],
            "promises": [],
            "mistakes": [],
            "wins": [],
            "habits": [],
            "motivation": [],
            "weaknesses": [],
            "strengths": [],
            "projects": [],
            "fears": [],
            "history": [],
            "observations": [],

            "progress": 0,

            "messages_today": 0,
            "reset_time": 0,

            "plan": "free",
            "pro_until": 0,
        }

        save_users()
      
    user = users[user_id]

    if user.get("step") == "done":
        await update.message.reply_text(
            "👋 С возвращением в ATLAS!",
            reply_markup=main_keyboard()
        )
        return
    
    await update.message.reply_text(
        "━━━━━━━━━━━━━━━━━━\n\n"
        "🤖 <b>Добро пожаловать в ATLAS</b>\n\n"
        "Твой персональный AI-помощник.\n\n"
        "<b>Я умею:</b>\n\n"
        "🧠 Запоминать важную информацию\n"
        "🎯 Помогать достигать целей\n"
        "🌐 Искать информацию в интернете\n"
        "📋 Составлять персональные планы\n"
        "🔥 Поддерживать мотивацию\n\n"
        "Давай познакомимся.\n\n"
        "👤 <b>Как тебя зовут?</b>\n\n"
        "━━━━━━━━━━━━━━━━━━",
        reply_markup=main_keyboard(),
        parse_mode="HTML"
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
    
    check_pro(user)
    
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
    
    if step == "change_name":
        user["name"] = text
        user["step"] = "done"

        save_users()

        await update.message.reply_text(
            f"✅ Имя изменено!\n\n👤 Теперь тебя зовут {text}"
        )
        return


    if step == "change_age":
        user["age"] = text
        user["step"] = "done"

        save_users()

        await update.message.reply_text(
            f"✅ Возраст обновлён!\n\n🎂 {text} лет"
        )
        return


    if step == "change_time":
        user["time"] = text
        user["step"] = "done"

        save_users()

        await update.message.reply_text(
            f"✅ Срок обновлён!\n\n⏳ {text}"
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
    
    if text == "⚙️ Настройки":
       user["step"] = "settings"
       save_users()

       await update.message.reply_text(
           "⚙️ Что ты хочешь изменить?\n\n"
           "• имя\n"
           "• возраст\n"
           "• цель\n"
           "• срок\n\n"
           "Напиши одно из этих слов."
       )
       return
    
    if step == "settings":

        if text.lower() == "имя":
            user["step"] = "change_name"
            save_users()

            await update.message.reply_text(
                "👤 Введи новое имя."
            )
            return

        elif text.lower() == "возраст":
            user["step"] = "change_age"
            save_users()

            await update.message.reply_text(
                "🎂 Введи новый возраст."
            )
            return

        elif text.lower() == "цель":
            user["step"] = "change_goal"
            save_users()

            await update.message.reply_text(
                "🎯 Введи новую цель."
            )
            return

        elif text.lower() == "срок":
            user["step"] = "change_time"
            save_users()

            await update.message.reply_text(
                "⏳ Введи новый срок."
            )
            return

        else:
            await update.message.reply_text(
                "Напиши:\n\n"
                "• имя\n"
                "• возраст\n"
                "• цель\n"
                "• срок"
            )
            return
    
    if step == "change_goal":
        user["goal"] = text
        user["step"] = "done"

        save_users()
 
        await update.message.reply_text(
            f"✅ Новая цель сохранена!\n\n🎯 {text}"
        )
        return
   
    if step == "change_name":
        user["name"] = text
        user["step"] = "done"
        
        save_users()

        await update.message.reply_text(
            f"✅ Имя изменено!\n\n👤 Теперь тебя зовут {text}"
        )
        return


    if step == "change_age":
        user["age"] = text
        user["step"] = "done"
        
        save_users()

        await update.message.reply_text(
            f"✅ Возраст обновлён!\n\n🎂 {text}"
        )
        return


    if step == "change_time":
        user["time"] = text
        user["step"] = "done"
        
        save_users()

        await update.message.reply_text(
            f"✅ Срок обновлён!\n\n⏳ {text}"
        )
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
            "━━━━━━━━━━━━━━━━━━\n\n"

            "🎉 <b>Регистрация завершена!</b>\n\n"

            "Добро пожаловать в <b>ATLAS</b> ❤️\n\n"

            "<b>Теперь я знаю:</b>\n\n"

            f"👤 {user.get('name')}\n"
            f"🎯 {user.get('goal')}\n"
            f"⏳ {user.get('time')}\n\n"

            "<b>Теперь я могу:</b>\n\n"

            "🧠 Запоминать важную информацию\n"
            "📋 Составлять персональные планы\n"
            "📈 Следить за прогрессом\n"
            "🌐 Искать информацию в интернете\n"
            "🔥 Помогать достигать целей\n\n"

            "💬 Просто напиши любой вопрос.\n\n"

            "🚀 Начнем!\n\n"

            "━━━━━━━━━━━━━━━━━━",
            parse_mode="HTML"
        )
       
        return



# ---------- AI (ИСПРАВЛЕНО ТУТ) ----------
    t = text.lower()

    # ---------- SMART MEMORY ----------
    memory_words = [
        "меня зовут",
        "мне",
        "мой",
        "моя",
        "моё",
        "люблю",
        "ненавижу",
        "хочу",
        "мечтаю",
        "работаю",
        "учусь",
        "живу",
        "родился",
        "цель",
        "семья",
        "девушка",
        "парень",
        "жена",
        "муж",
        "сын",
        "дочь",
        "любимое",
        "интересуюсь",
        "занимаюсь"
    ]

    if any(word in t for word in memory_words):
        if text not in user["facts"]:
            user["facts"].append(text)

    user["facts"] = user["facts"][-50:]
    
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
    analyze_user(user, text)
    
    add_message(user)
    save_users()
    
    try:
        answer = chat_ai(text, user["memory"], user)

        await update.message.reply_text(answer)

    except Exception as e:
        print("Ошибка:", e)

        await update.message.reply_text(
            "⚠️ Произошла небольшая ошибка.\n\n"
            "Попробуй повторить запрос через несколько секунд."
        )

    save_users()



# ---------- PROFILE ----------
async def profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_chat.id)

    if user_id not in users:
        await update.message.reply_text(
            "Сначала используй /start"
        )
        return

    user = users[user_id]

    tariff = "💎 PRO" if user.get("plan") == "pro" else "🆓 FREE"

    memory_count = len(user.get("facts", []))

    progress = get_progress(users, user_id)

    await update.message.reply_text(
        "━━━━━━━━━━━━━━━━━━\n\n"
        "👤 <b>ПРОФИЛЬ</b>\n\n"

        f"🙋 Имя: <b>{user.get('name','—')}</b>\n"
        f"🎂 Возраст: <b>{user.get('age','—')}</b>\n\n"

        f"🎯 Цель:\n<b>{user.get('goal','Не указана')}</b>\n\n"

        f"⏳ Срок:\n<b>{user.get('time','Не указан')}</b>\n\n"

        f"📈 Выполнено задач: <b>{progress}</b>\n"
        f"🧠 Запомнено фактов: <b>{memory_count}</b>\n"
        f"💳 Тариф: <b>{tariff}</b>\n"

        "\n━━━━━━━━━━━━━━━━━━",
        parse_mode="HTML"
    )



# ---------- HELP ----------
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "━━━━━━━━━━━━━━━━━━\n\n"

        "🤖 <b>ATLAS</b>\n\n"

        "Твой персональный AI-помощник.\n\n"

        "<b>Что умеет ATLAS:</b>\n\n"

        "🧠 Запоминает информацию о тебе\n"
        "🎯 Помогает достигать целей\n"
        "📋 Составляет планы\n"
        "📈 Следит за прогрессом\n"
        "🌐 Ищет информацию в интернете\n"
        "🔥 Мотивирует каждый день\n"
        "💎 Поддерживает PRO-подписку\n\n"

        "<b>Команды:</b>\n\n"

        "👤 /profile — профиль\n"
        "🎯 /goal — цель\n"
        "📈 /progress — прогресс\n"
        "📋 /plan — план\n"
        "🔥 /motivation — мотивация\n"
        "💎 /upgrade — PRO\n"
        "ℹ️ /help — помощь\n\n"

        "💬 Или просто напиши любой вопрос.\n\n"

        "━━━━━━━━━━━━━━━━━━",
        parse_mode="HTML"
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



# ---------- SETTINGS ----------
async def settings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "⚙️ Настройки ATLAS\n\n"

        "/change_name — изменить имя\n"
        "/change_goal — изменить цель\n"
        "/change_time — изменить срок\n"
        "/reset_memory — очистить память\n"
        "/restart — пройти регистрацию заново"
    )



# ---------- CHANGE GOAL ----------
async def change_goal_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_chat.id)

    if user_id not in users:
        await update.message.reply_text("Сначала используй /start")
        return

    users[user_id]["step"] = "change_goal"
    save_users()

    await update.message.reply_text(
        "🎯 Напиши новую цель."
    )
 


# ---------- RESTART ----------
async def restart(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
        "messages_today": users[user_id].get("messages_today", 0),
        "reset_time": users[user_id].get("reset_time", 0),
        "plan": users[user_id].get("plan", "free"),
        "pro_until": users[user_id].get("pro_until", 0),
    }

    save_users()

    await update.message.reply_text(
        "🔄 Регистрация сброшена.\n\n"
        "👤 Как тебя зовут?"
    )



# ---------- BUTTONS ----------
async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "buy_pro":
         await buy_pro(update, context)

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



# ---------- PAYMENTS ----------
async def precheckout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.pre_checkout_query.answer(ok=True)


async def successful_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_chat.id)

    activate_pro(users[user_id])
    save_users()

    await update.message.reply_text(
        "🎉 Спасибо за покупку!\n\n"
        "💎 PRO активирован на 30 дней."
    )


# ---------- APP ----------
app = Application.builder().token(TOKEN).build()

async def upgrade(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_chat.id)

    if user_id not in users:
        await update.message.reply_text("Сначала используй /start")
        return

    activate_pro(users[user_id])

    save_users()

    await update.message.reply_text(
        "💎 PRO активирован!\n\n"
        "📅 Подписка действует 30 дней.\n"
        "🚀 Спасибо за поддержку ATLAS ❤️"
    )

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("profile", profile))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(CommandHandler("plan", plan))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message))
app.add_handler(CommandHandler("upgrade", upgrade))
app.add_handler(CommandHandler("motivation", motivation))
app.add_handler(CommandHandler("goal", goal))
app.add_handler(CommandHandler("progress", progress))
app.add_handler(CommandHandler("done", done))
app.add_handler(CommandHandler("remind", remind))
app.add_handler(CommandHandler("settings", settings))
app.add_handler(CallbackQueryHandler(buttons))
app.add_handler(CommandHandler("change_goal", change_goal_command))
app.add_handler(CommandHandler("restart", restart))
app.add_handler(PreCheckoutQueryHandler(precheckout))
app.add_handler(
    MessageHandler(filters.SUCCESSFUL_PAYMENT, successful_payment)
)

print("🚀 ATLAS RUNNING")

async def post_init(application):
    asyncio.create_task(check_users(application.bot))

app.post_init = post_init

app.run_polling()