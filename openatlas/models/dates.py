from __future__ import annotations

from datetime import datetime
from typing import Any, Optional

import numpy


class Dates:
    def __init__(self, data: dict[str, Any]) -> None:
        self.begin_from = timestamp_to_datetime64(data.get('begin_from'))
        self.begin_to = timestamp_to_datetime64(data.get('begin_to'))
        self.begin_comment = data.get('begin_comment')
        self.end_from = timestamp_to_datetime64(data.get('end_from'))
        self.end_to = timestamp_to_datetime64(data.get('end_to'))
        self.end_comment = data.get('end_comment')
        self.first = format_date_part(self.begin_from, 'year') \
            if self.begin_from else None
        self.last = format_date_part(self.end_from, 'year') \
            if self.end_from else None
        self.last = format_date_part(self.end_to, 'year') \
            if self.end_to else None

    def to_timestamp(self) -> dict[str, Any]:
        from openatlas.display.util2 import sanitize
        return {
            'begin_from': datetime64_to_timestamp(self.begin_from),
            'begin_to':  datetime64_to_timestamp(self.begin_to),
            'begin_comment': sanitize(self.begin_comment),
            'end_from':  datetime64_to_timestamp(self.end_from),
            'end_to':  datetime64_to_timestamp(self.end_to),
            'end_comment': sanitize(self.end_comment)}


def timestamp_to_datetime64(string: str | None) -> numpy.datetime64 | None:
    if not string:
        return None
    string_list = string.split(' ')
    if 'BC' in string_list:
        parts = string_list[0].split('-')
        date = f'-{int(parts[0]) - 1}-{parts[1]}-{parts[2]}T{string_list[1]}'
        return numpy.datetime64(date)
    return numpy.datetime64(f'{string_list[0]}T{string_list[1]}')


def format_date_part(date: numpy.datetime64, part: str) -> str:
    string = str(date).split(' ', maxsplit=1)[0]
    bc = False
    if string.startswith('-') or string.startswith('0000'):
        bc = True
        string = string[1:]
    string = string.replace('T', '-').replace(':', '-')
    parts = string.split('-')
    if part == 'year':  # If it's a negative year, add one year
        return f'-{int(parts[0]) + 1}' if bc else f'{int(parts[0])}'
    if part == 'month':
        return parts[1]
    if part == 'hour':
        return parts[3]
    if part == 'minute':
        return parts[4]
    if part == 'second':
        return parts[5]
    return parts[2]


def datetime64_to_timestamp(date: Optional[numpy.datetime64]) -> Optional[str]:
    if not date:
        return None
    string = str(date)
    postfix = ''
    if string.startswith('-') or string.startswith('0000'):
        string = string[1:]
        postfix = ' BC'
    string = string.replace('T', '-').replace(':', '-').replace(' ', '-')
    parts = string.split('-')
    year = int(parts[0]) + 1 if postfix else int(parts[0])
    hour = 0
    minute = 0
    second = 0
    if len(parts) > 3:
        hour = int(parts[3])
        minute = int(parts[4])
        second = int(parts[5])
    return \
        f'{year:04}-{int(parts[1]):02}-{int(parts[2]):02} ' \
        f'{hour:02}:{minute:02}:{second:02}{postfix}'


def format_date(value: datetime | numpy.datetime64) -> str:
    if not value:
        return ''
    if isinstance(value, numpy.datetime64):
        date_ = datetime64_to_timestamp(value)
        return date_.lstrip('0').replace(' 00:00:00', '') if date_ else ''
    return value.date().isoformat().replace(' 00:00:00', '')


def check_if_entity_has_time(dates: Dates) -> bool:
    for date_ in [
            dates.begin_from,
            dates.begin_to,
            dates.end_from,
            dates.end_to]:
        if date_ and '00:00:00' not in str(date_):
            return True
    return False


def form_to_datetime64(
        year: Any,
        month: Any,
        day: Any,
        hour: Optional[Any] = None,
        minute: Optional[Any] = None,
        second: Optional[Any] = None,
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
        months_days: dict[int, int] = {
            1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31, 9: 30,
            10: 31, 11: 30, 12: 31}
        months_days_leap: dict[int, int] = {
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

    hour = f'{hour:02}' if hour else '00'
    minute = f'{minute:02}' if minute else '00'
    second = f'{second:02}' if second else '00'
    try:
        date_time = numpy.datetime64(
            f'{year}-{month}-{day}T{hour}:{minute}:{second}')
    except ValueError:
        return None
    return date_time
