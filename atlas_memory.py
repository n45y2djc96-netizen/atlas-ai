def analyze_user(user, text):
    t = text.lower()

    # Если каких-то полей нет — создаём
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

    # Общие факты
    fact_words = [
        "меня зовут",
        "мне",
        "мой",
        "моя",
        "моё",
        "люблю",
        "ненавижу",
        "живу",
        "работаю",
        "учусь",
        "интересуюсь",
        "занимаюсь"
    ]

    if any(word in t for word in fact_words):
        if text not in user["facts"]:
            user["facts"].append(text)

    # Мечты
    if any(word in t for word in [
        "мечтаю",
        "хочу",
        "хотел бы",
        "моя мечта"
    ]):
        if text not in user["dreams"]:
            user["dreams"].append(text)

    # Обещания
    if any(word in t for word in [
        "обещаю",
        "начну завтра",
        "завтра сделаю",
        "точно сделаю"
    ]):
        if text not in user["promises"]:
            user["promises"].append(text)

    # Победы
    if any(word in t for word in [
        "получилось",
        "сделал",
        "закончил",
        "добился",
        "смог"
    ]):
        if text not in user["wins"]:
            user["wins"].append(text)

    # Ошибки
    if any(word in t for word in [
        "не получилось",
        "сорвался",
        "бросил",
        "не сделал",
        "опять"
    ]):
        if text not in user["mistakes"]:
            user["mistakes"].append(text)

    # Страхи
    if any(word in t for word in [
        "боюсь",
        "страшно",
        "переживаю"
    ]):
        if text not in user["fears"]:
            user["fears"].append(text)

    # Ограничиваем память
    for field in fields:
        user[field] = user[field][-50:]