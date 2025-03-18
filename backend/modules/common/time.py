from datetime import datetime, timezone

from tzlocal import get_localzone


def get_current_timestamp() -> datetime:
    return datetime.now(tz=get_localzone())


def convert_to_local_timezone(timestamp: datetime) -> datetime:
    return timestamp.astimezone(tz=get_localzone())


def convert_to_utc_timezone(timestamp: datetime) -> datetime:
    return timestamp.astimezone(timezone.utc)
