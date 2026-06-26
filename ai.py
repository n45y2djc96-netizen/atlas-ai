import requests

API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-small"

headers = {
    "Authorization": "Bearer hf_ТВОЙ_ТОКЕН"
}

def chat_ai(text):
    try:
        response = requests.post(
            API_URL,
            headers=headers,
            json={"inputs": text}
        )

        data = response.json()

        if isinstance(data, list):
            return data[0].get("generated_text", "...")
        
        if isinstance(data, dict) and "error" in data:
            return "AI сейчас перегружен 😔"

        return str(data)

    except Exception as e:
        return "Ошибка AI 😔"