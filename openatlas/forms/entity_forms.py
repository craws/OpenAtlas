from typing import Any
from flask_babel import lazy_gettext as _
from openatlas.forms.base_form import BaseForm
from wtforms import (
    BooleanField, HiddenField, MultipleFileField,
    SelectField, SelectMultipleField, StringField, SubmitField, widgets)
from openatlas.forms.field import (
    TableField, TableMultiField, TreeField)


class AcquisitionForm(BaseForm):
    fields = ['name', 'date', 'description', 'continue']

    def additional_fields(self) -> dict[str, Any]:
        return {
            'event_id': HiddenField(),
            'event': TableField(_('sub event of')),
            'event_preceding': TableField(_('preceding event')),
            'place': TableField(_('location')),
            'given_place': TableMultiField(_('given place'))}
