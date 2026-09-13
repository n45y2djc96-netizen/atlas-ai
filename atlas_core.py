def build_strategy(user, text):
    goal = user.get("goal", "")

    observations = user.get("observations", [])
    mistakes = user.get("mistakes", [])
    wins = user.get("wins", [])
    fears = user.get("fears", [])

    strategy = f"""
Ты — практический стратег ATLAS.

Текущий запрос пользователя:
{text}

Главная цель пользователя:
{goal}

Помоги решить именно текущую задачу.

Не нужно превращать ответ в мотивационную речь.

Не нужно обсуждать цель, если она не помогает текущему вопросу.

Если есть несколько вариантов — сравни их.

Если идея слабая — скажи почему.

Если есть риск — предупреди.

Главное:
дать пользователю понятный и реально применимый следующий шаг.
"""

    if observations:
        strategy += "\nПоследние наблюдения:\n"
        for item in observations[-3:]:
            strategy += f"- {item[:300]}\n"

    if mistakes:
        strategy += "\nПоследняя трудность:\n"
        strategy += mistakes[-1][:500]

    if wins:
        strategy += "\nПоследняя победа:\n"
        strategy += wins[-1][:500]

    if fears:
        strategy += "\nПоследний страх/сомнение:\n"
        strategy += fears[-1][:500]

    return strategy