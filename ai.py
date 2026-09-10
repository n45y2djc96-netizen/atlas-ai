import os
from groq import Groq
from atlas_core import build_strategy
from atlas_brain import build_brain

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


SYSTEM_PROMPT = """
Ты — ATLAS, персональный AI-ассистент.

Твоя задача — не писать красивые статьи, а реально помогать человеку.

СТИЛЬ:
- Пиши живо, естественно и уверенно.
- Отвечай коротко по умолчанию.
- Обычно достаточно 2–6 предложений.
- Не пиши длинный ответ, если вопрос простой.
- Не используй таблицы без явной необходимости.
- Не начинай ответ с «🚀 Краткий вывод», «📌 Главное», «🛠 План действий».
- Не превращай каждый ответ в статью.
- Не повторяй вопрос пользователя.
- Не используй чрезмерно много эмодзи.
- Не обращайся к пользователю по имени в каждом сообщении.
- Не используй канцелярит.
- Не говори «как языковая модель».
- Не выдумывай факты.
- Если не знаешь — скажи прямо.
- Если вопрос простой, ответь просто.
- Если вопрос сложный, сначала дай суть, затем несколько конкретных пунктов.
- Если можно помочь следующим шагом, предложи его одной короткой фразой.

РАЗГОВОР:
Ты должен ощущаться как умный живой помощник, а не как учебник.
Не пытайся показать всё, что знаешь.
Показывай только то, что сейчас действительно полезно.

ПРИМЕР:

Пользователь: Что такое API?

Хороший ответ:
API — это способ, которым одна программа общается с другой.

Например, ATLAS отправляет запрос к AI-сервису через API и получает обратно ответ.

Пользователь: Как заработать миллион?

Хороший ответ:
Не ищи «секретную схему». Тебе нужен продукт, за который люди реально готовы платить.

Я бы начал с одной конкретной проблемы, сделал простой MVP и попытался получить первых 10 платящих клиентов.

Если хочешь, подберу 3 идеи именно под тебя.

ВАЖНО:
Если пользователь просит подробный разбор — тогда можешь отвечать подробно.
Если пользователь не просит подробностей — не растягивай ответ.
"""


def chat_ai(text, memory, user):
    try:
        messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            }
        ]

        # Только самые последние сообщения.
        # Это сильно уменьшает размер запроса.
        for msg in memory[-2:]:
            messages.append({
                "role": "user",
                "content": msg
            })

        # ---------------------------------
        # РОЛЬ ATLAS
        # ---------------------------------

        t = text.lower()

        role = ""

        if any(word in t for word in [
            "бизнес",
            "заработ",
            "деньги",
            "стартап",
            "инвест",
            "доход",
            "финанс",
            "миллион",
            "продать",
            "клиент"
        ]):
            role = """
Ты мыслишь как сильный предприниматель.
Давай конкретные идеи и следующие действия.
Не пиши мотивационные речи.
"""

        elif any(word in t for word in [
            "python",
            "код",
            "сайт",
            "бот",
            "программ",
            "ошибка",
            "telegram",
            "github"
        ]):
            role = """
Ты Senior Python Developer.
Объясняй просто.
Если пользователь просит исправить код — давай готовое решение.
Не пиши лишнюю теорию.
"""

        elif any(word in t for word in [
            "маркетинг",
            "реклама",
            "продажи",
            "клиенты",
            "бренд"
        ]):
            role = """
Ты сильный маркетолог.
Давай практичные идеи и конкретные действия.
"""

        elif any(word in t for word in [
            "спорт",
            "мышцы",
            "тренировка",
            "похудеть"
        ]):
            role = """
Ты опытный фитнес-наставник.
Отвечай понятно и безопасно.
"""

        if role:
            messages.append({
                "role": "system",
                "content": role
            })

        # ---------------------------------
        # ПРОФИЛЬ
        # ---------------------------------

        profile = []

        if user.get("name"):
            profile.append(f"Имя: {user['name']}")

        if user.get("age"):
            profile.append(f"Возраст: {user['age']}")

        if user.get("goal"):
            profile.append(f"Цель: {user['goal']}")

        if user.get("job"):
            profile.append(f"Работа: {user['job']}")

        if user.get("likes"):
            profile.append(
                "Интересы: " +
                ", ".join(user["likes"][-5:])
            )

        if profile:
            messages.append({
                "role": "system",
                "content":
                    "Короткая информация о пользователе:\n"
                    + "\n".join(profile)
            })

        # ---------------------------------
        # ПАМЯТЬ
        # ---------------------------------

        memory_info = []

        if user.get("dreams"):
            memory_info.append(
                "Мечты: " +
                "; ".join(user["dreams"][-2:])
            )

        if user.get("promises"):
            memory_info.append(
                "Обещания: " +
                "; ".join(user["promises"][-2:])
            )

        if user.get("wins"):
            memory_info.append(
                "Победы: " +
                "; ".join(user["wins"][-2:])
            )

        if user.get("insights"):
            memory_info.append(
                "Выводы: " +
                "; ".join(user["insights"][-2:])
            )

        if user.get("personality"):
            memory_info.append(
                "Личные ответы: " +
                "; ".join(user["personality"][-2:])
            )

        if memory_info:
            messages.append({
                "role": "system",
                "content":
                    "Полезная память о пользователе:\n"
                    + "\n".join(memory_info)
            })

        # ---------------------------------
        # STRATEGY
        # ---------------------------------

        strategy = build_strategy(user, text)

        if strategy:
            # Не позволяем стратегии раздувать запрос.
            strategy = strategy[:2500]

            messages.append({
                "role": "system",
                "content": strategy
            })

        # ---------------------------------
        # BRAIN
        # ---------------------------------

        brain = build_brain(user)

        if brain:
            # Ограничиваем дополнительный контекст.
            brain = brain[:2500]

            messages.append({
                "role": "system",
                "content": brain
            })

        # ---------------------------------
        # OBSERVATIONS
        # ---------------------------------

        if user.get("observations"):
            observations = user["observations"][-3:]

            messages.append({
                "role": "system",
                "content":
                    "Последние наблюдения ATLAS:\n"
                    + "\n".join(observations)
            })

        # ---------------------------------
        # ТЕКУЩИЙ ВОПРОС
        # ---------------------------------

        messages.append({
            "role": "user",
            "content": text
        })

        # ---------------------------------
        # GROQ
        # ---------------------------------

        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=messages,
            temperature=0.65,
            max_tokens=600
        )

        answer = response.choices[0].message.content.strip()

        return answer

    except Exception as e:
        print("ATLAS ERROR:", e)

        return (
            "Не получилось обработать запрос. "
            "Попробуй ещё раз через несколько секунд."
        )
