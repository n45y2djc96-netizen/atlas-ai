import random
from datetime import datetime

async def send_coach_message(bot, user_id, user):
    name = user.get("name", "друг")
    goal = user.get("goal", "своей цели")

    messages = [
        f"👋 {name}, как проходит твой день? Что ты уже сделал сегодня для цели: {goal}?",

        f"🎯 {name}, помни: твоя цель — {goal}. Какой один шаг ты можешь сделать прямо сейчас?",

        f"🚀 {name}, не жди идеального момента. Маленькое действие сегодня лучше, чем большой план завтра.",

        f"💪 {name}, я рядом, чтобы помочь тебе не сойти с пути. Что сейчас мешает двигаться к цели?",

        f"📈 {name}, каждый день без действия отдаляет тебя от цели. Давай сегодня сделаем хотя бы один шаг."
    ]

    await bot.send_message(
        chat_id=user_id,
        text=random.choice(messages)
    )