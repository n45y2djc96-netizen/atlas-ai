import os
from groq import Groq
from atlas_core import build_strategy

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def chat_ai(text, memory, user):
    try:
        messages = [
            {
                "role": "system",
                "content": """

Ты — ATLAS.

Ты дорогой персональный AI-помощник уровня ChatGPT Plus.

Главная задача — помогать пользователю получать результат, а не просто отвечать.

ПРАВИЛА

• Всегда будь уверен в своих ответах.
• Не используй фразы "мне кажется", "возможно", "наверное", "как языковая модель".
• Если информации недостаточно для точного ответа — сначала задай уточняющий вопрос.
• Отвечай красиво, профессионально и современно.
• Используй понятный, живой русский язык.
• Делай короткие абзацы для удобства чтения.
• Используй эмодзи только тогда, когда они делают ответ понятнее или приятнее.
• Используй заголовки и списки, если они улучшают восприятие ответа.
• Если можно предложить план действий — предложи пошаговый план.
• Не пиши длинные полотна текста без структуры.
• Если пользователь просит подробнее — отвечай максимально подробно.
• Если вопрос касается денег, бизнеса, заработка, инвестиций, продаж, маркетинга, стартапов или финансов — отвечай как опытный предприниматель.
• Если вопрос касается программирования — отвечай как Senior Python Developer.
• Если вопрос касается обучения — отвечай как опытный наставник.
• Если вопрос касается психологии — отвечай спокойно, уважительно и без осуждения.
• Если вопрос касается здоровья или права — предупреди, что окончательное решение лучше принимать после консультации со специалистом.
• Не выдумывай факты.
• Если чего-то не знаешь — честно скажи об этом и предложи возможное решение.
• Используй информацию, которую знаешь о пользователе, когда это помогает дать лучший ответ.
• Всегда выбирай наиболее удобный формат ответа в зависимости от вопроса.

ВЫБИРАЙ СТИЛЬ САМ.

Если вопрос простой:

например:
- Как меня зовут?
- Сколько мне лет?
- Какая моя цель?
- Что ты обо мне помнишь?

Отвечай коротко и естественно.

Пример:

😊 Тебя зовут Лев.

или

🎯 Твоя цель — стать миллиардером.

Не используй структуру для таких ответов.

Если пользователь просит:

• составить план
• что делать
• помочь разобраться
• объяснить
• сравнить
• проанализировать
• научить
• заработать
• открыть бизнес
• разработать стратегию

используй красивую структуру:

🚀 Краткий вывод

📌 Главное

• ...
• ...
• ...

🛠 План действий

1. ...
2. ...
3. ...

💡 Совет ATLAS

В остальных случаях отвечай обычным разговорным стилем, как дорогой персональный помощник.
"""

            }
        ]

        # Последние сообщения
        for msg in memory[-10:]:
            messages.append({
                "role": "user",
                "content": msg
            })

        # Выбор роли
        role = ""
        t = text.lower()

        if any(word in t for word in [
            "бизнес", "заработ", "деньги",
            "стартап", "инвест", "доход",
            "финанс", "миллион"
        ]):
            role = """
Ты опытный предприниматель.

Давай конкретные советы.

Думай как владелец успешной компании.

Предлагай реальные способы заработка.

Объясняй простым языком.
"""

        elif any(word in t for word in [
            "python", "код", "сайт",
            "бот", "программ", "ошибка",
            "telegram"
        ]):
            role = """
Ты Senior Python Developer.

Пиши качественный код.

Объясняй ошибки.

Всегда показывай готовое решение.
"""

        elif any(word in t for word in [
            "маркетинг", "реклама",
            "продажи", "клиенты", "бренд"
        ]):
            role = """
Ты опытный маркетолог.

Предлагай современные способы продвижения.

Используй реальные стратегии.
"""

        elif any(word in t for word in [
            "спорт", "мышцы",
            "тренировка", "похудеть",
            "здоровье"
        ]):
            role = """
Ты профессиональный фитнес-тренер.

Давай понятные рекомендации.

Не советуй опасные вещи.
"""

        if role:
            messages.append({
                "role": "system",
                "content": role
            })

        # Память пользователя
        profile = ""

        if user.get("name"):
            profile += f"Имя: {user['name']}\n"

        if user.get("age"):
            profile += f"Возраст: {user['age']}\n"

        if user.get("goal"):
            profile += f"Цель: {user['goal']}\n"

        if user.get("job"):
            profile += f"Работа: {user['job']}\n"

        if user.get("cat"):
            profile += f"Кот: {user['cat']}\n"

        if user.get("dog"):
            profile += f"Собака: {user['dog']}\n"

        if user.get("likes"):
            profile += "Интересы:\n"
            for i in user["likes"]:
                profile += f"- {i}\n"

        if profile:
            messages.append({
                "role": "system",
                "content": f"Информация о пользователе:\n{profile}"
            })

        # Память ATLAS
        memory_info = ""

        if user.get("dreams"):
            memory_info += "Мечты пользователя:\n"
            for i in user["dreams"][-5:]:
                memory_info += f"- {i}\n"

        if user.get("promises"):
            memory_info += "\nОбещания пользователя:\n"
            for i in user["promises"][-5:]:
                memory_info += f"- {i}\n"

        if user.get("wins"):
            memory_info += "\nПоследние победы:\n"
            for i in user["wins"][-5:]:
                memory_info += f"- {i}\n"

        if user.get("mistakes"):
            memory_info += "\nОшибки:\n"
            for i in user["mistakes"][-5:]:
                memory_info += f"- {i}\n"

        if user.get("fears"):
            memory_info += "\nСтрахи:\n"
            for i in user["fears"][-5:]:
                memory_info += f"- {i}\n"
       
        if user.get("insights"):
            memory_info += "\nВыводы ATLAS о пользователе:\n"
            for i in user["insights"][-5:]:
                memory_info += f"- {i}\n"
        
        if memory_info:
            messages.append({
                "role": "system",
                "content": memory_info
            })
       
        strategy = build_strategy(user, text)

        messages.append({
            "role": "system",
            "content": strategy
        })
        
        brain = build_brain(user)

        messages.append({
            "role": "system",
            "content": brain
        })
        
        # Новый вопрос
        messages.append({
            "role": "user",
            "content": text
        })
         # Анализ личности ATLAS

        if user.get("observations"):

            messages.append({
                "role": "system",
                "content":
                "Наблюдения ATLAS о пользователе:\n\n"
                + "\n".join(user["observations"])
            })
        
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0.5,
            max_tokens=2048
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"❌ Ошибка: {e}"