def analyze_user(user, text):
    text = text.lower()

    # Жалобы
    if any(word in text for word in [
        "не могу",
        "не получается",
        "устал",
        "лень",
        "боюсь",
        "нет сил",
        "не хочу"
    ]):
        user.setdefault("mistakes", []).append(text)

    # Победы
    if any(word in text for word in [
        "сделал",
        "получилось",
        "выполнил",
        "закончил",
        "добился"
    ]):
        user.setdefault("wins", []).append(text)

    # Мотивация
    if any(word in text for word in [
        "мечта",
        "хочу",
        "миллиардер",
        "успех"
    ]):
        user.setdefault("motivation", []).append(text)

    # Определяем риск срыва
    mistakes = len(user.get("mistakes", []))
    wins = len(user.get("wins", []))

    if mistakes >= wins + 3:
        user["risk_level"] = "high"
    else:
        user["risk_level"] = "low"