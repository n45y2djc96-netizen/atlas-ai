import time


LIMIT = 10
RESET_SECONDS = 86400


def init_user(user):
    if "messages_today" not in user:
        user["messages_today"] = 0

    if "reset_time" not in user:
        user["reset_time"] = 0

    if "plan" not in user:
        user["plan"] = "free"


def check_reset(user):
    now = int(time.time())

    if user["reset_time"] == 0:
        user["reset_time"] = now + RESET_SECONDS

    if now >= user["reset_time"]:
        user["messages_today"] = 0
        user["reset_time"] = now + RESET_SECONDS
        return True

    return False


def can_send(user):
    if user["plan"] == "pro":
        return True

    return user["messages_today"] < LIMIT


def add_message(user):
    user["messages_today"] += 1