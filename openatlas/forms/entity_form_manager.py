from typing import Any
from flask_babel import lazy_gettext as _

from openatlas.models.link import Link
from openatlas.forms.base_form_manager import BaseFormManager
from wtforms import HiddenField
from openatlas.forms.field import TableField, TableMultiField


class EventBaseForm(BaseFormManager):
    fields = ['name', 'date', 'description', 'continue']

    def additional_fields(self) -> dict[str, Any]:
        fields = {
            'event_id': HiddenField(),
            'event': TableField(_('sub event of')),
            'event_preceding': TableField(_('preceding event'))}
        if self.class_.name != 'move':
            fields['place'] = TableField(_('location'))
        return fields

    def populate_update(self) -> None:
        super().populate_update()
        self.form.event_id.data = self.entity.id
        if super_event := self.entity.get_linked_entity('P9'):
            self.form.event.data = super_event.id
        if preceding_event := self.entity.get_linked_entity('P134', True):
            self.form.event_preceding.data = preceding_event.id
        if self.class_.name != 'move':
            if place := self.entity.get_linked_entity('P7'):
                self.form.place.data = \
                    place.get_linked_entity_safe('P53', True).id

    def process_form_data(self):
        super().process_form_data()
        self.data['links']['delete'].append('P9')
        self.data['links']['delete_inverse'].append('P134')
        self.data['links']['insert'].append({
            'property': 'P9',
            'range': self.form.event.data})
        self.data['links']['insert'].append({
            'property': 'P134',
            'range': self.form.event_preceding.data,
            'inverse': True})
        if self.class_.name != 'move':
            self.data['links']['delete'].append('P7')
            if self.form.place.data:
                self.data['links']['insert'].append({
                    'property': 'P7',
                    'range': Link.get_linked_entity_safe(
                        int(self.form.place.data),
                        'P53')})


class AcquisitionForm(EventBaseForm):

    def additional_fields(self) -> dict[str, Any]:
        return dict(super().additional_fields(), **{
            'given_place': TableMultiField(_('given place'))})

    def populate_update(self) -> None:
        super().populate_update()
        self.form.given_place.data = [
            entity.id for entity in self.entity.get_linked_entities('P24')]

    def process_form_data(self):
        super().process_form_data()
        self.data['links']['delete'].append('P24')
        self.data['links']['insert'].append({
            'property': 'P24',
            'range': self.form.given_place.data})


class ActivityForm(EventBaseForm):
    pass


class EventForm(EventBaseForm):
    pass


class MoveForm(EventBaseForm):

    def additional_fields(self) -> dict[str, Any]:
        return dict(super().additional_fields(), **{
            'place_from': TableField(_('from')),
            'place_to': TableField(_('to')),
            'artifact': TableMultiField(),
            'person': TableMultiField()})

    def process_form_data(self):
        super().process_form_data()
        self.data['links']['delete'] += ['P25', 'P26', 'P27']
        if self.form.artifact.data:
            self.data['links']['insert'].append({
                'property': 'P25',
                'range': self.form.artifact.data})
        if self.form.person.data:
            self.data['links']['insert'].append({
                'property': 'P25',
                'range': self.form.person.data})
        if self.form.place_from.data:
            self.data['links']['insert'].append({
                'property': 'P27',
                'range': Link.get_linked_entity_safe(
                    int(self.form.place_from.data),
                    'P53')})
        if self.form.place_to.data:
            self.data['links']['insert'].append({
                'property': 'P26',
                'range': Link.get_linked_entity_safe(
                    int(self.form.place_to.data),
                    'P53')})

    def populate_update(self) -> None:
        super().populate_update()
        if place_from := self.entity.get_linked_entity('P27'):
            self.form.place_from.data = \
                place_from.get_linked_entity_safe('P53', True).id
        if place_to := self.entity.get_linked_entity('P26'):
            self.form.place_to.data = \
                place_to.get_linked_entity_safe('P53', True).id
        person_data = []
        object_data = []
        for linked_entity in self.entity.get_linked_entities('P25'):
            if linked_entity.class_.name == 'person':
                person_data.append(linked_entity.id)
            elif linked_entity.class_.view == 'artifact':
                object_data.append(linked_entity.id)
        self.form.person.data = person_data
        self.form.artifact.data = object_data


class ProductionForm(EventBaseForm):

    def additional_fields(self) -> dict[str, Any]:
        return dict(super().additional_fields(), **{
            'artifact': TableMultiField()})

    def process_form_data(self):
        super().process_form_data()
        self.data['links']['delete'].append('P108')
        self.data['links']['insert'].append({
                'property': 'P108',
                'range': self.form.artifact.data})

    def populate_update(self) -> None:
        super().populate_update()
        self.form.artifact.data = \
            [entity.id for entity in self.entity.get_linked_entities('P108')]
