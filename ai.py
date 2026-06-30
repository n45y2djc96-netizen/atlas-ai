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
                    "Отвечай понятно, подробно и дружелюбно."
                )
            }
        ]

        for msg in memory[-10:]:
            messages.append({
                "role": "user",
                "content": msg
            })

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