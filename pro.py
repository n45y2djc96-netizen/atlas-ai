import time

PRO_TIME = 30 * 24 * 60 * 60  # 30 дней


def activate_pro(user):
    user["plan"] = "pro"
    user["pro_until"] = int(time.time()) + PRO_TIME


def check_pro(user):
    if user.get("plan") != "pro":
        return

    if int(time.time()) >= user.get("pro_until", 0):
        user["plan"] = "free"
        user["pro_until"] = 0