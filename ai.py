import os
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def chat_ai(text, memory, user):
    try:
        messages = [
            {
                "role": "system",
                "content": (
                    "Ты ATLAS — умный AI-помощник. "
                    "Отвечай понятно, подробно и дружелюбно. "
                    "Помогай с бизнесом, программированием, учебой, "
                    "саморазвитием и любыми другими вопросами."
                )
            }
        ]

        # Последние сообщения
        for msg in memory[-10:]:
            messages.append({
                "role": "user",
                "content": msg
            })

        # Память о пользователе
        facts = "\n".join(user.get("facts", []))

        if facts:
            messages.append({
                "role": "system",
                "content": f"Запомни пользователя:\n{facts}"
            })

        # Новый вопрос
        messages.append({
            "role": "user",
            "content": text
        })

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0.7,
            max_tokens=1024
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"❌ Ошибка: {e}"