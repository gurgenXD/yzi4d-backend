from datetime import datetime
from zoneinfo import ZoneInfo

def datetime_format(value: datetime) -> str:
    """Формат даты и времени."""
    return value.astimezone(tz=ZoneInfo("Europe/Moscow")).strftime("%d.%m.%Y %H:%M:%S")
