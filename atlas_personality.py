def remember_personality(user, text):
    t = text.lower()

    if "personality" not in user:
        user["personality"] = []

    personal_words = [
        "мечтаю",
        "люблю",
        "горжусь",
        "боюсь",
        "мне нравится",
        "для меня важно",
        "моя мечта",
        "я ненавижу",
        "мне нравится",
        "не люблю"
    ]

    if any(word in t for word in personal_words):
        if text not in user["personality"]:
            user["personality"].append(text)

    user["personality"] = user["personality"][-30:]