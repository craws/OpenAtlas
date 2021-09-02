from typing import Any, Dict, Optional, TYPE_CHECKING

import numpy

if TYPE_CHECKING:  # pragma: no cover - Type checking is disabled in tests
    pass


def timestamp_to_datetime64(string: str) -> Optional[numpy.datetime64]:
    if not string:
        return None
    if 'BC' in string:
        parts = string.split(' ')[0].split('-')
        string = f'-{int(parts[0]) - 1}-{parts[1]}-{parts[2]}'
    return numpy.datetime64(string.split(' ')[0])


def datetime64_to_timestamp(date: numpy.datetime64) -> Optional[str]:
    if not date:
        return None
    string = str(date)
    postfix = ''
    if string.startswith('-') or string.startswith('0000'):
        string = string[1:]
        postfix = ' BC'
    parts = string.split('-')
    year = int(parts[0]) + 1 if postfix else int(parts[0])
    return f'{year:04}-{int(parts[1]):02}-{int(parts[2]):02}{postfix}'


def form_to_datetime64(
        year: Any,
        month: Any,
        day: Any,
        to_date: bool = False) -> Optional[numpy.datetime64]:
    if not year:
        return None
    year = year if year > 0 else year + 1

    def is_leap_year(year_: int) -> bool:
        if year_ % 400 == 0:  # e.g. 2000
            return True
        if year_ % 100 == 0:  # e.g. 1000
            return False
        if year_ % 4 == 0:  # e.g. 1996
            return True
        return False

    def get_last_day_of_month(year_: int, month_: int) -> int:
        months_days: Dict[int, int] = {
            1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31, 9: 30,
            10: 31, 11: 30, 12: 31}
        months_days_leap: Dict[int, int] = {
            1: 31, 2: 29, 3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31, 9: 30,
            10: 31, 11: 30, 12: 31}
        date_lookup = months_days_leap \
            if is_leap_year(year_) else months_days
        return date_lookup[month_]

    if month:
        month = f'{month:02}'
    elif to_date:
        month = '12'
    else:
        month = '01'

    if day:
        day = f'{day:02}'
    elif to_date:
        day = f'{get_last_day_of_month(int(year), int(month)):02}'
    else:
        day = '01'

    try:
        date_time = numpy.datetime64(f'{year}-{month}-{day}')
    except ValueError:
        return None
    return date_time
