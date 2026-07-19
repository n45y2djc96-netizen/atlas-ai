def check_focus(user, text):
    text = text.lower()

    goal = user.get("goal", "").lower()

    if goal == "":
        return None

    off_topic = [
        "тикток",
        "ютуб",
        "игра",
        "сериал",
        "ленюсь",
        "ничего не делаю",
        "скучно",
        "не хочу работать"
    ]

    if any(word in text for word in off_topic):
        return (
            f"🎯 Помни, твоя главная цель — {user['goal']}.\n\n"
            "То, о чём ты сейчас говоришь, может немного увести тебя в сторону.\n\n"
            "Какой один небольшой шаг ты можешь сделать уже сегодня, чтобы приблизиться к своей цели?"
        )

    return None