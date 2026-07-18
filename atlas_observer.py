def observe_user(user):

    observations = []

    if len(user.get("mistakes", [])) >= 3:
        observations.append(
            "Пользователь часто сталкивается с одними и теми же ошибками."
        )

    if len(user.get("wins", [])) >= 3:
        observations.append(
            "Пользователь умеет доводить начатое до конца."
        )

    if len(user.get("promises", [])) > len(user.get("wins", [])):
        observations.append(
            "Пользователь часто обещает больше, чем выполняет."
        )

    if len(user.get("wins", [])) > len(user.get("mistakes", [])):
        observations.append(
            "Последнее время пользователь показывает хороший прогресс."
        )

    user["observations"] = observations