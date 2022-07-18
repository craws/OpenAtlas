from typing import Any

from openatlas.forms.util import form_to_datetime64


def process_form_dates(form) -> dict[str, Any]:
    data = {
        'begin_from': None, 'begin_to': None, 'begin_comment': None,
        'end_from': None, 'end_to': None, 'end_comment': None}
    if hasattr(form, 'begin_year_from') and form.begin_year_from.data:
        data['begin_comment'] = form.begin_comment.data
        data['begin_from'] = form_to_datetime64(
            form.begin_year_from.data,
            form.begin_month_from.data,
            form.begin_day_from.data,
            form.begin_hour_from.data if 'begin_hour_from' in form else None,
            form.begin_minute_from.data if 'begin_hour_from' in form else None,
            form.begin_second_from.data if 'begin_hour_from' in form else None)
        data['begin_to'] = form_to_datetime64(
            form.begin_year_to.data,
            form.begin_month_to.data,
            form.begin_day_to.data,
            form.begin_hour_to.data if 'begin_hour_from' in form else None,
            form.begin_minute_to.data if 'begin_hour_from' in form else None,
            form.begin_second_to.data if 'begin_hour_from' in form else None,
            to_date=True)
    if hasattr(form, 'end_year_from') and form.end_year_from.data:
        data['end_comment'] = form.end_comment.data
        data['end_from'] = form_to_datetime64(
            form.end_year_from.data,
            form.end_month_from.data,
            form.end_day_from.data,
            form.end_hour_from.data if 'begin_hour_from' in form else None,
            form.end_minute_from.data if 'begin_hour_from' in form else None,
            form.end_second_from.data if 'begin_hour_from' in form else None)
        data['end_to'] = form_to_datetime64(
            form.end_year_to.data,
            form.end_month_to.data,
            form.end_day_to.data,
            form.end_hour_to.data if 'begin_hour_from' in form else None,
            form.end_minute_to.data if 'begin_hour_from' in form else None,
            form.end_second_to.data if 'begin_hour_from' in form else None,
            to_date=True)
    return data
