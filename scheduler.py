import asyncio
import json
import time

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

            if user.get("plan") == "pro":
                continue

            if user.get("reset_time", 0) == 0:
                continue

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

        if changed:
            save_users(users)

        await asyncio.sleep(300)