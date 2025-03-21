from datetime import datetime, timezone
from os import environ

from dateutil import tz

TIME_ZONE = environ["TZ"]


def get_current_timestamp() -> datetime:
    return datetime.now(tz=tz.gettz(TIME_ZONE))


def convert_timestamp_to_local_timestamp(timestamp: datetime) -> datetime:
    return timestamp.astimezone(tz=tz.gettz(TIME_ZONE))


def convert_timestamp_to_utc_timestamp(timestamp: datetime) -> datetime:
    return timestamp.astimezone(timezone.utc)
