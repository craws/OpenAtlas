from typing import Any
from flask_babel import lazy_gettext as _

from openatlas.forms.base_manager import BaseManager, EventBaseManager
from openatlas.models.link import Link
from openatlas.forms.field import TableField, TableMultiField


class AcquisitionManager(EventBaseManager):

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


class ActivityManager(EventBaseManager):
    pass


class ArtifactManager(BaseManager):
    fields = ['name', 'date', 'description', 'continue', 'map']

    def additional_fields(self) -> dict[str, Any]:
        return {'actor': TableField(_('owned by'))}

    def populate_update(self) -> None:
        super().populate_update()
        if owner := self.entity.get_linked_entity('P52'):
            self.form.actor.data = owner.id

    def process_form_data(self):
        super().process_form_data()
        self.data['gis'] = {}
        for shape in ['point', 'line', 'polygon']:
            self.data['gis'][shape] = getattr(self.form, f'gis_{shape}s').data
        self.data['links']['delete'].append('P52')
        if self.form.actor.data:
            self.data['links']['insert'].append({
                'property': 'P52',
                'range': self.form.actor.data})


class BibliographyManager(BaseManager):
    fields = ['name', 'description', 'continue']


class EditionManager(BaseManager):
    fields = ['name', 'description', 'continue']


class EventManager(EventBaseManager):
    pass


class ExternalReferenceManager(BaseManager):
    fields = ['url', 'description', 'continue']


class HumanRemainsManager(BaseManager):
    fields = ['name', 'date', 'description', 'continue', 'map']

    def additional_fields(self) -> dict[str, Any]:
        return {'actor': TableField(_('owned by'))}

    def populate_update(self) -> None:
        super().populate_update()
        if owner := self.entity.get_linked_entity('P52'):
            self.form.actor.data = owner.id

    def process_form_data(self):
        super().process_form_data()
        self.data['gis'] = {}
        for shape in ['point', 'line', 'polygon']:
            self.data['gis'][shape] = getattr(self.form, f'gis_{shape}s').data
        self.data['links']['delete'].append('P52')
        if self.form.actor.data:
            self.data['links']['insert'].append({
                'property': 'P52',
                'range': self.form.actor.data})


class MoveManager(EventBaseManager):

    def additional_fields(self) -> dict[str, Any]:
        return dict(super().additional_fields(), **{
            'place_from': TableField(_('from')),
            'place_to': TableField(_('to')),
            'artifact': TableMultiField(),
            'person': TableMultiField()})

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


class ProductionManager(EventBaseManager):

    def additional_fields(self) -> dict[str, Any]:
        return dict(super().additional_fields(), **{
            'artifact': TableMultiField()})

    def populate_update(self) -> None:
        super().populate_update()
        self.form.artifact.data = \
            [entity.id for entity in self.entity.get_linked_entities('P108')]

    def process_form_data(self):
        super().process_form_data()
        self.data['links']['delete'].append('P108')
        self.data['links']['insert'].append({
            'property': 'P108',
            'range': self.form.artifact.data})
