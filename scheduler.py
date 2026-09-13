import asyncio
import json
import time

DATA_FILE = "users.json"


def load_users():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def save_users(users):
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(
                users,
                f,
                ensure_ascii=False,
                indent=2
            )
    except Exception as e:
        print("SCHEDULER SAVE ERROR:", e)


async def check_users(bot):
    while True:
        try:
            users = load_users()
            changed = False
            now = int(time.time())

            for user_id, user in users.items():

                # Проверяем только сброс бесплатного лимита.
                if user.get("plan") == "pro":
                    continue

                reset_time = user.get("reset_time", 0)

                if reset_time and now >= reset_time:
                    user["messages_today"] = 0
                    user["reset_time"] = 0
                    changed = True

                    try:
                        await bot.send_message(
                            chat_id=int(user_id),
                            text=(
                                "🎉 Бесплатный доступ снова открыт!\n\n"
                                "Можешь продолжить пользоваться ATLAS."
                            )
                        )
                    except Exception:
                        pass

            if changed:
                save_users(users)

        except Exception as e:
            print("SCHEDULER ERROR:", e)

        await asyncio.sleep(300)