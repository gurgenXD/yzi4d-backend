from datetime import UTC, date, datetime


def calculate_ages(start_date: date) -> int:
    """Посчитать пройденные года."""
    today = datetime.now(tz=UTC).date()
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
