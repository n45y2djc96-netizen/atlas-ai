def analyze_user(user, text):
    t = text.lower().strip()

    fields = [
        "facts",
        "dreams",
        "promises",
        "mistakes",
        "wins",
        "habits",
        "motivation",
        "weaknesses",
        "strengths",
        "projects",
        "fears",
        "history",
        "observations"
    ]

    for field in fields:
        if field not in user:
            user[field] = []

    # ФАКТЫ О ПОЛЬЗОВАТЕЛЕ
    fact_phrases = [
        "меня зовут",
        "я учусь",
        "я работаю",
        "я живу",
        "я занимаюсь",
        "я интересуюсь",
        "я люблю",
        "я не люблю",
        "мой любимый",
        "моя любимая"
    ]

    if any(phrase in t for phrase in fact_phrases):
        if text not in user["facts"]:
            user["facts"].append(text)

    # МЕЧТЫ
    dream_phrases = [
        "я мечтаю",
        "моя мечта",
        "хочу когда-нибудь",
        "хотел бы когда-нибудь"
    ]

    if any(phrase in t for phrase in dream_phrases):
        if text not in user["dreams"]:
            user["dreams"].append(text)

    # ПОБЕДЫ
    win_phrases = [
        "у меня получилось",
        "я сделал",
        "я закончил",
        "я смог",
        "я добился",
        "всё получилось"
    ]

    if any(phrase in t for phrase in win_phrases):
        if text not in user["wins"]:
            user["wins"].append(text)

    # ОШИБКИ
    mistake_phrases = [
        "не получилось",
        "я сорвался",
        "я не сделал",
        "я бросил",
        "опять не получилось"
    ]

    if any(phrase in t for phrase in mistake_phrases):
        if text not in user["mistakes"]:
            user["mistakes"].append(text)

    # СТРАХИ
    fear_phrases = [
        "я боюсь",
        "мне страшно",
        "я переживаю",
        "я сильно переживаю"
    ]

    if any(phrase in t for phrase in fear_phrases):
        if text not in user["fears"]:
            user["fears"].append(text)

    for field in fields:
        user[field] = user[field][-50:]