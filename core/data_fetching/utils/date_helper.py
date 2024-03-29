from datetime import date, time, datetime, timedelta


def utc_today() -> date:  # pragma: no cover
    utc = datetime.utcnow()
    return date(utc.year, utc.month, utc.day)


def get_prev_17lands_update_time() -> datetime:  # pragma: no cover
    utc = datetime.utcnow()
    dt = datetime.combine(utc_today(), time(2, 0))
    if dt > utc:
        dt -= timedelta(days=1)
    return dt


def get_next_17lands_update_time() -> datetime:  # pragma: no cover
    ret = get_prev_17lands_update_time() + timedelta(days=1)
    return ret
