import os
import requests

API_KEY = os.getenv("OPENROUTER_API_KEY")

API_URL = "https://openrouter.ai/api/v1/chat/completions"


def chat_ai(text, memory, user):
    try:
        messages = [
            {
                "role": "system",
                "content": (
                    "Ты ATLAS — умный AI-помощник. "
                    "Помогаешь с бизнесом, заработком, саморазвитием, "
                    "обучением и отвечаешь как настоящий AI."
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

        response = requests.post(
            API_URL,
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "openrouter/auto",
                "messages": messages
            },
            timeout=60
        )

        if response.status_code != 200:
            return f"❌ Ошибка {response.status_code}\n{response.text}"

        data = response.json()

        return data["choices"][0]["message"]["content"]
        
    except Exception as e:
        return f"❌ Ошибка: {e}"