from telegram import ReplyKeyboardMarkup

def main_keyboard():
    keyboard = [
        ["🎯 Цель", "📈 Прогресс"],
        ["🔥 Мотивация", "📋 План"],
        ["💎 PRO"]
    ]

    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True
    )