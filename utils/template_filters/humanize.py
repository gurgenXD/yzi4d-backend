from datetime import date, datetime

import pytz


def calculate_ages(start_date: date) -> int:
    """Посчитать пройденные года."""
    target_time_zone = pytz.timezone("Europe/Moscow")
    today = datetime.now(tz=target_time_zone).date()
    return today.year - start_date.year


def humanize_age(age: int) -> str:
    """Очеловечивание возраста."""
    if age % 100 in (11, 12, 13, 14):
        return f"{age} лет"

    if age % 10 == 1:
        return f"{age} год"

    if age % 10 in (2, 3, 4):
        return f"{age} года"

    return f"{age} лет"
