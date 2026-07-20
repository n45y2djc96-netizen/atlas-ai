def remember_promise(user, text):
    t = text.lower()

    triggers = [
        "завтра",
        "начну",
        "сделаю",
        "обещаю",
        "буду",
        "планирую",
        "хочу начать"
    ]

    if any(i in t for i in triggers):

        if "promises" not in user:
            user["promises"] = []

        user["promises"].append(text)
        user["promises"] = user["promises"][-30:]
