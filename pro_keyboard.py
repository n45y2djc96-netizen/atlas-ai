from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def pro_keyboard():
    keyboard = [
        [InlineKeyboardButton("💎 Купить PRO", callback_data="buy_pro")],
        [InlineKeyboardButton("⏰ Напомнить завтра", callback_data="remind_me")]
    ]

    return InlineKeyboardMarkup(keyboard)