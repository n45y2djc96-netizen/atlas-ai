def need_internet(text):
    text = text.lower()

    words = [
        "сегодня",
        "сейчас",
        "последние",
        "новости",
        "погода",
        "курс",
        "цена",
        "bitcoin",
        "btc",
        "доллар",
        "евро",
        "акции",
        "крипто",
        "матч",
        "счет",
        "результат",
        "когда вышел",
        "что произошло",
        "что нового"
    ]

    return any(word in text for word in words)