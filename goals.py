def change_goal(users, user_id, new_goal):
    if user_id not in users:
        return "❌ Пользователь не найден"

    users[user_id]["goal"] = new_goal
    return f"🎯 Новая цель сохранена:\n\n{new_goal}"


def get_goal(users, user_id):
    if user_id not in users:
        return "❌ Пользователь не найден"

    return users[user_id].get("goal", "Цель не указана")