def observe_user(user):

    observations = []

    mistakes = user.get("mistakes", [])
    wins = user.get("wins", [])
    promises = user.get("promises", [])

    # Частые ошибки
    if len(mistakes) >= 3:
        observations.append(
            "Пользователь часто сталкивается с одними и теми же ошибками."
        )

    # Хороший прогресс
    if len(wins) >= 3:
        observations.append(
            "Пользователь умеет доводить начатое до конца."
        )

    # Много обещаний, мало результатов
    if len(promises) > len(wins):
        observations.append(
            "Пользователь часто обещает больше, чем выполняет."
        )

    # Последнее время есть прогресс
    if len(wins) > len(mistakes):
        observations.append(
            "Последнее время пользователь показывает хороший прогресс."
        )

    # Определяем риск срыва
    risk = "low"

    if len(mistakes) >= 5 and len(wins) < 2:
        risk = "high"
        observations.append(
            "Высокий риск срыва: пользователь часто сталкивается с неудачами и редко фиксирует победы."
        )

    elif len(mistakes) > len(wins):
        risk = "medium"
        observations.append(
            "Средний риск срыва: ошибок больше, чем побед."
        )

    user["observations"] = observations
    user["risk_level"] = risk