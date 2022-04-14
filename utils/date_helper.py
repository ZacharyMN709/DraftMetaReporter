from datetime import date, time, datetime, timedelta


def get_prev_17lands_update_time() -> datetime:
    utc = datetime.utcnow()
    dt = datetime.combine(utc_today(), time(2, 0))
    if dt > utc:
        dt -= timedelta(days=1)
    return dt


def get_next_17lands_update_time() -> datetime:
    return get_prev_17lands_update_time() + timedelta(days=1)


def utc_today() -> date:
    utc = datetime.utcnow()
    return date(utc.year, utc.month, utc.day)
