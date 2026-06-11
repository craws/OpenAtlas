from pathlib import Path
from typing import Any

from flask import g, request
from flask_babel import gettext as _
from flask_wtf import FlaskForm

from openatlas.models.dates import form_to_datetime64


def file(_form: FlaskForm, field: Any) -> None:
    for file_ in request.files.getlist('file'):  # pylint: disable=no-member
        if not file_ \
                or Path(str(file_.filename)).suffix[1:].lower() not in [
                    i.lower() for i in
                    g.settings['file_upload_allowed_extension']]:
            field.errors.append(_('file type not allowed'))


def validate(form: FlaskForm, extra_validators: Any = None) -> bool:
    valid = FlaskForm.validate(form, extra_validators)
    if hasattr(form, 'begin_year_from') and not validate_dates(form):
        valid = False
    for field_id, field in form.__dict__.items():
        if field_id.startswith('reference_system_id_') \
                and field.data \
                and field.data['value']:
            if not field.data['precision']:
                valid = False
                field.errors.append(_('precision required'))
            match field.label.text:
                case 'Wikidata':
                    if field.data['value'][0] != 'Q' \
                            or not field.data['value'][1:].isdigit():
                        field.errors.append(_('wrong id format'))
                        valid = False
                case 'GeoNames':
                    if not field.data['value'].isnumeric():
                        field.errors.append(_('wrong id format'))
                        valid = False
    return valid


def validate_dates(form: FlaskForm) -> bool:
    valid = True
    dates = {}
    for prefix in ['begin_', 'end_']:
        for postfix in ['_from', '_to']:
            if getattr(form, f'{prefix}year{postfix}').data:
                date = form_to_datetime64(
                    getattr(form, f'{prefix}year{postfix}').data,
                    getattr(form, f'{prefix}month{postfix}').data,
                    getattr(form, f'{prefix}day{postfix}').data,
                    getattr(form, f'{prefix}hour{postfix}').data
                    if f'{prefix}hour{postfix}' in form else None,
                    getattr(form, f'{prefix}minute{postfix}').data
                    if f'{prefix}minute{postfix}' in form else None,
                    getattr(form, f'{prefix}second{postfix}').data
                    if f'{prefix}second{postfix}' in form else None,
                    to_date=postfix == '_to')
                if not date:
                    getattr(form, f'{prefix}day{postfix}').errors.append(
                        _('not a valid date'))
                    valid = False
                    continue
                dates[prefix + postfix.replace('_', '')] = date

    # Check for valid date combination e.g. begin not after end
    if valid:
        for prefix in ['begin', 'end']:
            if f'{prefix}_from' in dates \
                    and f'{prefix}_to' in dates \
                    and dates[f'{prefix}_from'] > dates[f'{prefix}_to']:
                field = getattr(form, f'{prefix}_year_from')
                field.errors.append(_('First date cannot be after second.'))
                valid = False
    has_begin = 'begin_from' in dates or 'begin_to' in dates
    has_end = 'end_from' in dates or 'end_to' in dates
    if valid and has_begin and has_end:
        begin = dates['begin_to'] \
            if 'begin_to' in dates else dates['begin_from']
        end = dates['end_from'] if 'end_from' in dates else dates['end_to']
        if begin > end:
            getattr(form, 'begin_year_from').errors.append(
                _('Begin dates cannot start after end dates.'))
            valid = False
    return valid
