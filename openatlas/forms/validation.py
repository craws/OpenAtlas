from pathlib import Path
from typing import Any

from flask import g, request
from flask_babel import lazy_gettext as _
from flask_wtf import FlaskForm

from openatlas.models.dates import form_to_datetime64


def file(_form: FlaskForm, field: Any) -> None:
    for file_ in request.files.getlist('file'):
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
        if getattr(form, f'{prefix}year_to').data \
                and not getattr(form, f'{prefix}year_from').data:
            getattr(form, f'{prefix}year_from').errors.append(
                _("Required for time span"))
            valid = False
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
                    if f'{prefix}second{postfix}' in form else None)
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
    if 'begin_from' in dates and 'end_from' in dates:
        field = getattr(form, 'begin_year_from')
        if len(dates) == 4 and (
                dates['begin_from'] > dates['end_from']
                or dates['begin_to'] > dates['end_to']):
            field.errors.append(_('Begin dates cannot start after end dates.'))
            valid = False
        elif len(dates) != 4:
            first = dates['begin_to'] \
                if 'begin_to' in dates else dates['begin_from']
            second = dates['end_from'] \
                if 'end_from' in dates else dates['end_to']
            if first > second:
                field.errors.append(
                    _('Begin dates cannot start after end dates.'))
                valid = False
    return valid
