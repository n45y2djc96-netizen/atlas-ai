import asyncio
import json
import time
from atlas_coach import send_coach_message

DATA_FILE = "users.json"


def load_users():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}


def save_users(users):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)


async def check_users(bot):
    while True:

        users = load_users()

        changed = False
        now = int(time.time())

        for user_id, user in users.items():

            # Отправляем инициативное сообщение раз в день
            last_message = user.get("last_coach_message", 0)

            if now - last_message >= 86400:  # 24 часа
                try:
                    await send_coach_message(bot, user_id, user)
                    user["last_coach_message"] = now
                    changed = True
                except:
                    pass

            # Проверяем только бесплатных пользователей
            if user.get("plan") == "pro":
                continue

            if user.get("reset_time", 0) == 0:
                continue

            # Сбрасываем лимит через 24 часа
            if now >= user["reset_time"]:

                user["messages_today"] = 0
                user["reset_time"] = 0

                changed = True

                try:
                    await bot.send_message(
                        chat_id=int(user_id),
                        text=(
                            "🎉 Бесплатный доступ снова открыт!\n\n"
                            "Рады видеть тебя снова ❤️\n\n"
                            "🚀 Можешь продолжить пользоваться ATLAS."
                        )
                    )
                except:
                    pass

        # Сохраняем изменения один раз после всех проверок
        if changed:
            save_users(users)

        # Проверяем пользователей каждые 5 минут
        await asyncio.sleep(300)