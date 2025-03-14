from datetime import datetime, timezone


def get_current_utc_timestamp() -> datetime:
    return datetime.now(tz=timezone.utc)
