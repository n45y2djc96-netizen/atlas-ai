import requests

API_URL = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium"

headers = {
    "Authorization": "Bearer ТВОЙ_HF_ТОКЕН"
}


def chat_ai(text, memory=None):
    try:
        if memory is None:
            memory = []

        # Берём последние сообщения пользователя
        context = "\n".join(memory[-5:])
        prompt = f"{context}\nПользователь: {text}\nATLAS:"

        response = requests.post(
            API_URL,
            headers=headers,
            json={"inputs": prompt},
            timeout=30
        )

        data = response.json()

        if isinstance(data, list):
            return data[0].get("generated_text", "🤖 Не знаю что ответить.")

        if isinstance(data, dict) and "error" in data:
            return "⏳ AI сейчас загружается. Попробуй ещё раз."

        return "🤖 Не удалось получить ответ."

    except Exception as e:
        return "❌ Ошибка подключения AI."