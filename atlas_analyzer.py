def analyze_user(user, text):
    t = text.lower()

    # пользователь что-то обещает
    if any(x in t for x in [
        "обещаю",
        "завтра сделаю",
        "начну завтра",
        "точно сделаю"
    ]):
        user["promises"].append(text)

    # говорит про успех
    if any(x in t for x in [
        "сделал",
        "получилось",
        "готово",
        "закончил",
        "смог"
    ]):
        user["wins"].append(text)

    # говорит про ошибки
    if any(x in t for x in [
        "не получилось",
        "сорвался",
        "не сделал",
        "ленился",
        "отложил"
    ]):
        user["mistakes"].append(text)

    # страхи
    if any(x in t for x in [
        "боюсь",
        "страшно",
        "не уверен",
        "сомневаюсь"
    ]):
        user["fears"].append(text)

    # мотивация
    if any(x in t for x in [
        "мечтаю",
        "хочу",
        "хочу добиться",
        "моя цель"
    ]):
        user["dreams"].append(text)

    # ограничиваем память
    for key in [
        "promises",
        "wins",
        "mistakes",
        "dreams",
        "fears"
    ]:
        user[key] = user[key][-50:]