def update_memory(user, text):
    text = text.strip()

    if "меня зовут" in text.lower():
        user["name"] = text.split()[-1]

    elif "мне " in text.lower() and "лет" in text.lower():
        user["age"] = text

    elif "я работаю" in text.lower():
        user["job"] = text

    elif "моя цель" in text.lower():
        user["goal"] = text

    elif "я люблю" in text.lower():
        user.setdefault("likes", []).append(text)

    elif "мой любимый" in text.lower():
        user.setdefault("likes", []).append(text)

    elif "мой кот" in text.lower():
        user["cat"] = text

    elif "моя собака" in text.lower():
        user["dog"] = text

    return user