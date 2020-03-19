from math import modf
from datetime import datetime, timedelta


def get_datetime(year, month, day, hour, minute, second_float):
    """Return datetime object with given arguments. If argument second
    contains a value larger than or equal to 60, convert it to a valid
    value by taking its modulo against 60 and adding one minute to the
    datetime. Handle invalid minute values (>= 60) similarly.

    Keyword arguments:
    year -- Year as an integer
    month -- Month as an integer
    day -- Day as an integer
    hour -- Hour as an integer
    minute -- Minute as an integer
    second_float -- Seconda and microsecond as a float
    """
    second_parts = modf(second_float)
    second = int(second_parts[1])
    microsecond = int(second_parts[0] * 1000000)

    if second >= 60:
        second = second % 60
        date = datetime(
            year, month, day, hour, minute, second, microsecond
        )
        date = date + timedelta(minutes=1)
        return date

    if minute >= 60:
        minute = minute % 60
        date = datetime(
            year, month, day, hour, minute, second, microsecond
        )
        date = date + timedelta(hours=1)
        return date

    return datetime(
        year, month, day, hour, minute, second, microsecond
    )
