from datetime import datetime, timedelta
from zoneinfo import ZoneInfo


def datetime_format(value: datetime) -> str:
    """Формат даты и времени."""
    return value.astimezone(tz=ZoneInfo("Europe/Moscow")).strftime("%d.%m.%Y %H:%M:%S")


def timedelta_format(value: timedelta) -> str:
    """Формат разницы времени."""
    hours, remainder = divmod(value.total_seconds(), 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:.0f}:{minutes:.0f}:{seconds:.1f}"
