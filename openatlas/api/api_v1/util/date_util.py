from typing import Any


def is_leap_year(year: int) -> bool:
    abs_year = abs(year)
    if abs_year % 400 == 0:
        return True
    if abs_year % 100 == 0:
        return False
    if abs_year % 4 == 0:
        return True
    return False


def get_last_day_of_month(year: int, month: int) -> int:
    if month == 2:
        return 29 if is_leap_year(year) else 28
    if month in (4, 6, 9, 11):
        return 30
    return 31


def handle_date(value: Any, is_end_date: bool = False) -> str | None:
    if value is None:
        return None
    value_str = str(value).strip()
    if not value_str:
        return None

    is_negative = False
    if value_str.startswith('-'):
        is_negative = True
        value_str = value_str[1:].strip()

    parts = value_str.split('-')
    if not parts or not parts[0].isdigit():
        raise ValueError(f"Invalid date format: {value}")

    year_int = int(parts[0])
    year_str = f"{year_int:04d}"
    if is_negative:
        year_str = f"-{year_str}"

    if len(parts) == 1:
        if is_end_date:
            return f"{year_str}-12-31"
        return f"{year_str}-01-01"

    if len(parts) == 2:
        month_int = int(parts[1])
        if not (1 <= month_int <= 12):
            raise ValueError(f"Invalid month: {month_int} in date {value}")
        month_str = f"{month_int:02d}"
        if is_end_date:
            last_day = get_last_day_of_month(year_int, month_int)
            return f"{year_str}-{month_str}-{last_day:02d}"
        return f"{year_str}-{month_str}-01"

    if len(parts) == 3:
        month_int = int(parts[1])
        day_int = int(parts[2])
        if not (1 <= month_int <= 12):
            raise ValueError(f"Invalid month: {month_int} in date {value}")
        last_day = get_last_day_of_month(year_int, month_int)
        if not (1 <= day_int <= last_day):
            raise ValueError(
                f"Invalid day: {day_int} for month {month_int} in date {value}")
        return f"{year_str}-{month_int:02d}-{day_int:02d}"

    raise ValueError(f"Invalid date format: {value}")
