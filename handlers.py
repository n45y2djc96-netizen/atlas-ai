async def upgrade(update, context):
    user_id = str(update.effective_chat.id)

    result = activate_pro(users, user_id)
    save_users(users)

    await update.message.reply_text(result)