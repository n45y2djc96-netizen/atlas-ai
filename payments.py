def activate_pro(users, user_id):
    if user_id not in users:
        return "❌ Пользователь не найден"

    users[user_id]["plan"] = "pro"
    return "💎 PRO активирован! Теперь у тебя полный доступ"


def is_pro(users, user_id):
    return users.get(user_id, {}).get("plan") == "pro"
    