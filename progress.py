def add_progress(users, user_id):
    if user_id not in users:
        return "❌ Пользователь не найден"

    if "progress" not in users[user_id]:
        users[user_id]["progress"] = 0

    users[user_id]["progress"] += 1

    return (
        f"🔥 Прогресс сохранён!\n"
        f"Всего выполнено шагов: "
        f"{users[user_id]['progress']}"
    )


def get_progress(users, user_id):
    if user_id not in users:
        return "❌ Пользователь не найден"

    return users[user_id].get("progress", 0)