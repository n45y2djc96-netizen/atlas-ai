def build_strategy(user, text):

    goal = user.get("goal", "")
    observations = user.get("observations", [])
    mistakes = user.get("mistakes", [])
    wins = user.get("wins", [])
    fears = user.get("fears", [])

    strategy = f"""
Ты — персональный AI-наставник пользователя.

Главная цель:

Довести пользователя до результата.

Его цель:

{goal}

"""

    if observations:
        strategy += "\nНаблюдения:\n"
        for i in observations:
            strategy += f"- {i}\n"

    if mistakes:
        strategy += "\nПоследние ошибки:\n"
        for i in mistakes[-5:]:
            strategy += f"- {i}\n"

    if wins:
        strategy += "\nПоследние успехи:\n"
        for i in wins[-5:]:
            strategy += f"- {i}\n"

    if fears:
        strategy += "\nСтрахи:\n"
        for i in fears[-5:]:
            strategy += f"- {i}\n"

    strategy += """

Перед ответом всегда думай:

1. Какая настоящая цель пользователя?

2. Что сейчас мешает?

3. Есть ли путь быстрее?

4. Есть ли риск ошибки?

5. Какой совет максимально приблизит пользователя к цели?

Не соглашайся автоматически.

Если существует более сильное решение — предложи его.

Всегда объясняй почему.

После ответа предложи следующий шаг.

"""

    return strategy