def remember_promise(user, text):
    t = text.lower()

    triggers = [
        "обещаю",
        "завтра точно сделаю",
        "завтра сделаю",
        "точно сделаю",
        "сделаю это завтра",
        "начну завтра"
    ]

    if any(word in t for word in triggers):

        if "promises" not in user:
            user["promises"] = []

        if text not in user["promises"]:
            user["promises"].append(text)

        user["promises"] = user["promises"][-30:]
        