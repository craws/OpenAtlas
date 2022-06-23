from typing import Any
from flask_babel import lazy_gettext as _
from openatlas.forms.base_form_manager import BaseFormManager
from wtforms import HiddenField
from openatlas.forms.field import TableField, TableMultiField


class AcquisitionForm(BaseFormManager):
    fields = ['name', 'date', 'description', 'continue']

    def additional_fields(self) -> dict[str, Any]:
        return {
            'event_id': HiddenField(),
            'event': TableField(_('sub event of')),
            'event_preceding': TableField(_('preceding event')),
            'place': TableField(_('location')),
            'given_place': TableMultiField(_('given place'))}
