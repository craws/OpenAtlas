from typing import Any
from flask_babel import lazy_gettext as _

from openatlas.models.link import Link
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

    def populate_update(self) -> None:
        super().populate_update()
        self.form.event_id.data = self.entity.id
        self.form.given_place.data = [
            entity.id for entity in self.entity.get_linked_entities('P24')]
        if super_event := self.entity.get_linked_entity('P9'):
            self.form.event.data = super_event.id
        if preceding_event := self.entity.get_linked_entity('P134', True):
            self.form.event_preceding.data = preceding_event.id
        if place := self.entity.get_linked_entity('P7'):
            self.form.place.data = place.get_linked_entity_safe('P53', True).id

    def process_form_data(self):
        super().process_form_data()
        self.data['links']['delete'].update(['P7', 'P9', 'P24'])
        self.data['links']['delete_inverse'].add('P134')
        self.data['links']['insert'].append({
            'property': 'P24',
            'range': self.form.given_place.data})
        self.data['links']['insert'].append({
            'property': 'P9',
            'range': self.form.event.data})
        self.data['links']['insert'].append({
            'property': 'P134',
            'range': self.form.event_preceding.data,
            'inverse': True})
        if self.form.place.data:
            self.data['links']['insert'].append({
                'property': 'P7',
                'range': Link.get_linked_entity_safe(
                    int(self.form.place.data),
                    'P53')})
