def remember_personality(user, text):
    t = text.lower()

    if "personality" not in user:
        user["personality"] = []

    # Личные темы, которые стоит запоминать
    personal_words = [
        "мечтаю", "люблю", "горжусь", "боюсь",
        "хочу", "нравится", "важно", "счастлив",
        "семья", "друзья", "детство", "будущее"
    ]

    if any(word in t for word in personal_words):
        if text not in user["personality"]:
            user["personality"].append(text)

    # Храним только последние 30 личных ответов
    user["personality"] = user["personality"][-30:]