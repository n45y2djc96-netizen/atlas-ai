import time
import random

async def check_promises(bot, users):
    now = int(time.time())

    for user_id, user in users.items():
        promises = user.get("promises", [])

        if not promises:
            continue

        # Проверяем последнее обещание
        last_promise = promises[-1]

        # Когда в последний раз спрашивали об обещании
        last_check = user.get("last_promise_check", 0)

        # Спрашиваем раз в 2 дня
        if now - last_check >= 172800:
            name = user.get("name", "друг")

            messages = [
                f"{name}, ты говорил: «{last_promise}». Получилось продвинуться в этом?",

                f"{name}, я помню твоё обещание: «{last_promise}». Что уже сделано?",

                f"{name}, несколько дней назад ты сказал: «{last_promise}». Давай честно — получилось выполнить это?"
            ]

            try:
                await bot.send_message(
                    chat_id=int(user_id),
                    text=random.choice(messages)
                )

                user["last_promise_check"] = now

            except:
                pass