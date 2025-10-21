from __future__ import annotations, annotations

from typing import Any, Optional

from flask import g, url_for
from flask_babel import format_number, lazy_gettext as _

from openatlas import app
from openatlas.display.tab import Tab
from openatlas.display.util import button, link
from openatlas.models.entity import Entity, Link


class BaseDisplay:
    buttons: list[str]
    data: dict[str, Any]
    tabs: dict[str, Tab]

    def __init__(self, entity: Entity) -> None:
        self.entity = entity
        self.events: list[Entity] = []
        self.event_links: Optional[list[Link]] = []
        self.linked_places: list[Entity] = []
        self.structure: dict[str, list[Entity]] = {}
        self.gis_data: dict[str, Any] = {}
        self.problematic_type = self.entity.check_too_many_single_type_links()


class PlaceBaseDisplay(BaseDisplay):

    def add_tabs(self) -> None:
        self.tabs['event'] = Tab('event', entity=self.entity)
        if self.entity.class_.name == 'place':
            self.tabs['actor'] = Tab('actor', entity=self.entity)


class TypeBaseDisplay(BaseDisplay):

    def add_data(self) -> None:
        if self.entity.category == 'value':
            self.data[_('unit')] = self.entity.description
        self.data[_('selectable')] = str(_('yes')) \
            if self.entity.selectable else str(_('no'))
        self.data[_('ID for imports')] = self.entity.id

    def add_tabs(self) -> None:
        entity = self.entity
        self.tabs['subs'] = Tab('subs', entity=entity)
        self.tabs['entities'] = Tab('entities', entity=entity)
        self.tabs['file'] = Tab('file', entity=entity)
        self.tabs['reference'] = Tab('reference', entity=entity)
        for sub_id in entity.subs:
            self.tabs['subs'].table.rows.append([
                link(g.types[sub_id]),
                g.types[sub_id].count,
                g.types[sub_id].description])
        if entity.category == 'value':
            self.tabs['entities'].table.columns = \
                [_('name'), _('value'), _('class'), _('info')]
        classes_ = [
            'feature',
            'stratigraphic_unit',
            'artifact',
            'human_remains']
        possible_sub_unit = False
        if any(item in g.types[entity.root[0]].classes for item in classes_):
            possible_sub_unit = True
            self.tabs['entities'].table.columns.append('place')
        root = g.types[entity.root[0]] if entity.root else entity
        if root.name in app.config['PROPERTY_TYPES']:
            self.tabs['entities'].table.columns = [_('domain'), _('range')]
            for row in Link.get_links_by_type(entity):
                self.tabs['entities'].table.rows.append([
                    link(Entity.get_by_id(row['domain_id'])),
                    link(Entity.get_by_id(row['range_id']))])
        else:
            entities = entity.get_linked_entities(
                ['P2', 'P89'],
                inverse=True,
                types=True,
                sort=True)
            root_places = {}
            if possible_sub_unit and entities:
                root_places = Entity.get_roots(
                    'P46',
                    [e.id for e in entities],
                    inverse=True)
            for item in entities:
                if item.class_.name == 'object_location':
                    item = item.get_linked_entity_safe('P53', inverse=True)
                data = [link(item)]
                if entity.category == 'value':
                    data.append(format_number(item.types[entity]))
                data.append(item.class_.label)
                data.append(item.description)
                data.append(
                    link(
                        root_places[item.id]['name'],
                        url_for('view', id_=root_places[item.id]['id']))
                    if item.id in root_places else '')
                self.tabs['entities'].table.rows.append(data)
        if root.category not in ['system', 'value'] \
                and self.tabs['entities'].table.rows:
            self.tabs['entities'].buttons.append(
                button(
                    _('move entities'),
                    url_for('type_move_entities', id_=entity.id)))


class PlaceDisplay(PlaceBaseDisplay):

    def add_tabs(self) -> None:
        if self.entity.location:
            for link_ in self.entity.location.get_links(
                    ['P74', 'OA8', 'OA9'],
                    inverse=True):
                actor = Entity.get_by_id(link_.domain.id)
                self.tabs['actor'].table.rows.append([
                    link(actor),
                    g.properties[link_.property.code].name,
                    actor.class_.name,
                    actor.first,
                    actor.last,
                    actor.description])
        actor_ids = []
        for event in self.events:
            for actor in \
                    event.get_linked_entities(
                        ['P11', 'P14', 'P22', 'P23'],
                        sort=True):
                if actor.id not in actor_ids:
                    actor_ids.append(actor.id)
                    self.tabs['actor'].table.rows.append([
                        link(actor),
                        f"{_('participated at an event')}",
                        event.class_.name, '', '', ''])
