from telegram import LabeledPrice

PRICE = 199


async def buy_pro(update, context):
    await context.bot.send_invoice(
        chat_id=update.effective_chat.id,
        title="ATLAS PRO",
        description="Подписка ATLAS PRO на 30 дней",
        payload="atlas_pro",
        provider_token="",
        currency="XTR",
        prices=[
            LabeledPrice("ATLAS PRO", PRICE)
        ]
    )