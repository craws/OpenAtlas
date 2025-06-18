from __future__ import annotations

from typing import Any, Optional

from flask import g, url_for
from flask_babel import format_number, lazy_gettext as _
from flask_login import current_user

from openatlas import app
from openatlas.display.tab import Tab
from openatlas.display.util import (
    button, edit_link, format_entity_date, get_appearance, get_base_table_data,
    get_chart_data, link, profile_image_table_link, remove_link)
from openatlas.display.util2 import (
    is_authorized, uc_first)
from openatlas.models.entity import Entity, Link
from openatlas.models.gis import Gis
from openatlas.models.overlay import Overlay


class BaseDisplay:
    buttons: list[str]
    crumbs: list[Any]
    data: dict[str, Any]
    overlays = None
    tabs: dict[str, Tab]

    def __init__(self, entity: Entity) -> None:
        self.entity = entity
        self.events: list[Entity] = []
        self.event_links: Optional[list[Link]] = []
        self.linked_places: list[Entity] = []
        self.structure: dict[str, list[Entity]] = {}
        self.gis_data: dict[str, Any] = {}
        self.problematic_type = self.entity.check_too_many_single_type_links()
        self.entity.image_id = entity.get_profile_image_id()


class ActorDisplay(BaseDisplay):

    def add_data(self) -> None:
        if begin_place := self.entity.get_linked_entity('OA8'):
            begin_object = begin_place.get_linked_entity_safe('P53', True)
            self.linked_places.append(begin_object)
            self.data[_('begin')] = \
                format_entity_date(self.entity, 'begin', begin_object)
        if end_place := self.entity.get_linked_entity('OA9'):
            end_object = end_place.get_linked_entity_safe('P53', True)
            self.linked_places.append(end_object)
            self.data[_('end')] = \
                format_entity_date(self.entity, 'end', end_object)
        if residence := self.entity.get_linked_entity('P74'):
            residence_object = residence.get_linked_entity_safe('P53', True)
            self.linked_places.append(residence_object)
            self.data[_('residence')] = link(residence_object)
        if self.event_links:
            appears_first, appears_last = get_appearance(self.event_links)
            self.data[_('appears first')] = appears_first
            self.data[_('appears last')] = appears_last

    def add_tabs(self) -> None:
        entity = self.entity
        for name in [
                'source', 'event', 'relation', 'member_of', 'member',
                'artifact', 'reference', 'file']:
            if entity.class_.name == 'group' or name != 'member':
                self.tabs[name] = Tab(name, entity=entity)
        self.tabs['member_of'].label = uc_first(_('member of'))
        self.tabs['relation'].label = uc_first(_('relation'))
        if 'member' in self.tabs:
            self.tabs['member'].label = uc_first(_('member'))
        # self.add_reference_tables_data()
        self.event_links = \
            entity.get_links(['P11', 'P14', 'P22', 'P23', 'P25'], True)
        for link_ in self.event_links:
            event = link_.domain
            link_.object_ = None  # Needed for first/last appearance
            for place in event.get_linked_entities(
                    ['P7', 'P26', 'P27'],
                    sort=True):
                link_.object_ = place.get_linked_entity_safe('P53', True)
                self.linked_places.append(link_.object_)
            self.tabs['event'].table.rows.append([
                link(event),
                event.class_.label,
                _('moved')
                if link_.property.code == 'P25' else link(link_.type),
                link_.first or (
                    f'<span class="text-muted">{event.first}</span>'
                    if event.first else ''),
                link_.last or (
                    f'<span class="text-muted">{event.last}</span>'
                    if event.last else ''),
                link_.description,
                '' if link_.property.code == 'P25' else
                edit_link(
                    url_for('link_update', id_=link_.id, origin_id=entity.id)),
                remove_link(link_.domain.name, link_, entity, 'event')])
        for link_ in entity.get_links('OA7') + entity.get_links('OA7', True):
            related = link_.range \
                if entity.id == link_.domain.id else link_.domain
            self.tabs['relation'].table.rows.append([
                '' if not link_.type else link(
                    link_.type.get_name_directed(entity.id != link_.domain.id),
                    url_for('view', id_=link_.type.id)),
                link(related),
                link_.first,
                link_.last,
                link_.description,
                edit_link(
                    url_for('link_update', id_=link_.id, origin_id=entity.id)),
                remove_link(related.name, link_, entity, 'relation')])
        for link_ in entity.get_links('P107', True):
            self.tabs['member_of'].table.rows.append([
                link(link_.domain),
                link(link_.type),
                link_.first,
                link_.last,
                link_.description,
                edit_link(
                    url_for('link_update', id_=link_.id, origin_id=entity.id)),
                remove_link(link_.domain.name, link_, entity, 'member-of')])
        for link_ in entity.get_links('P52', True):
            self.tabs['artifact'].table.rows.append([
                link(link_.domain),
                link_.domain.class_.label,
                link(link_.domain.standard_type),
                link_.domain.first,
                link_.domain.last,
                link_.domain.description])


class EventsDisplay(BaseDisplay):

    def add_data(self) -> None:
        self.data[_('sub event of')] = \
            link(self.entity.get_linked_entity('P9', inverse=True))
        self.data[_('preceding event')] = \
            link(self.entity.get_linked_entity('P134'))
        self.data[_('succeeding event')] = \
            '<br>'.join([
                link(e)
                for e in self.entity.get_linked_entities(
                    'P134',
                    inverse=True,
                    sort=True)])
        if place := self.entity.get_linked_entity('P7'):
            self.data[_('location')] = \
                link(place.get_linked_entity_safe('P53', True))

    def add_tabs(self) -> None:
        entity = self.entity
        for name in ['subs', 'source', 'actor', 'reference', 'file']:
            self.tabs[name] = Tab(name, entity=entity)
        # self.add_reference_tables_data()
        for sub in entity.get_linked_entities('P9', types=True, sort=True):
            self.tabs['subs'].table.rows.append(get_base_table_data(sub))
        self.tabs['actor'].table.header.insert(5, _('activity'))
        for link_ in entity.get_links(['P11', 'P14', 'P22', 'P23']):
            self.tabs['actor'].table.rows.append([
                link(link_.range),
                link_.range.class_.label,
                link_.type.name if link_.type else '',
                link_.first
                or f'<span class="text-muted">{entity.first}</span>'
                if entity.first else '',
                link_.last or f'<span class="text-muted">{entity.last}</span>'
                if entity.last else '',
                g.properties[link_.property.code].name_inverse,
                link_.description,
                edit_link(
                    url_for('link_update', id_=link_.id, origin_id=entity.id)),
                remove_link(link_.range.name, link_, entity, 'actor')])
        self.linked_places = [
            location.get_linked_entity_safe('P53', True) for location
            in entity.get_linked_entities(['P7', 'P26', 'P27'], sort=True)]


class PlaceBaseDisplay(BaseDisplay):

    # def add_button_delete(self) -> None:
    #    if not self.entity.get_linked_entities('P46'):
    #        super().add_button_delete()

    def add_tabs(self) -> None:
        entity = self.entity
        for name in ['source', 'event', 'reference', 'artifact']:
            self.tabs[name] = Tab(name, entity=entity)
        if entity.class_.name == 'place':
            self.tabs['actor'] = Tab('actor', entity=entity)
            self.tabs['feature'] = Tab('feature', entity=entity)
        elif entity.class_.name == 'feature':
            self.tabs['stratigraphic_unit'] = Tab(
                'stratigraphic_unit',
                _('stratigraphic unit'),
                entity=entity)
        self.tabs['file'] = Tab('file', entity=entity)
        if entity.class_.view == 'place' \
                and is_authorized('editor') \
                and current_user.settings['module_map_overlay']:
            self.tabs['file'].table.header.append(_('overlay'))

        for link_ in entity.get_links(['P31', 'P67'], inverse=True):
            domain = link_.domain
            if domain.class_.view == 'reference_system':
                entity.reference_systems.append(link_)
                continue
            data = get_base_table_data(domain)
            if domain.class_.view in ['event']:
                self.tabs[domain.class_.view].table.rows.append(data)
                continue
            if domain.class_.view == 'file':
                ext = data[6]
                data.append(profile_image_table_link(entity, domain, ext))
                if not entity.image_id and ext in g.display_file_ext:
                    entity.image_id = domain.id
                if entity.class_.view == 'place' \
                        and is_authorized('editor') \
                        and current_user.settings['module_map_overlay']:
                    content = ''
                    if ext in app.config['DISPLAY_FILE_EXT']:
                        overlays = Overlay.get_by_object(entity)
                        if domain.id in overlays and (html_link := edit_link(
                                url_for(
                                    'overlay_update',
                                    place_id=entity.id,
                                    overlay_id=overlays[domain.id].id))):
                            content += html_link
                        else:
                            content = link(
                                _('link'),
                                url_for(
                                    'overlay_insert',
                                    image_id=domain.id,
                                    place_id=entity.id,
                                    link_id=link_.id))
                    data.append(content)
            if domain.class_.view not in ['source', 'file']:
                data.append(link_.description)
                data.append(edit_link(
                    url_for('link_update', id_=link_.id, origin_id=entity.id)))
            data.append(
                remove_link(domain.name, link_, entity, domain.class_.view))
            self.tabs[domain.class_.view].table.rows.append(data)

        entity.location = entity.get_linked_entity_safe('P53', types=True)
        event_ids = []  # Keep track of event ids to prevent event doubles
        for event in \
                entity.get_linked_entities(
                    ['P24', 'P25', 'P108'],
                    inverse=True) + \
                entity.location.get_linked_entities(
                    ['P7', 'P26', 'P27'],
                    inverse=True):
            if event.id not in event_ids:
                self.events.append(event)
                self.tabs['event'].table.rows.append(
                    get_base_table_data(event))
                event_ids.append(event.id)
        self.structure = entity.get_structure()
        if self.structure:
            for item in self.structure['subunits']:
                name = 'artifact' if item.class_.view == 'artifact' \
                    else item.class_.name
                self.tabs[name].table.rows.append(get_base_table_data(item))
        self.gis_data = Gis.get_all([entity], self.structure)
        if self.gis_data['gisPointSelected'] == '[]' \
                and self.gis_data['gisPolygonSelected'] == '[]' \
                and self.gis_data['gisLineSelected'] == '[]' \
                and (not self.structure or not self.structure['supers']):
            self.gis_data = {}


class ReferenceBaseDisplay(BaseDisplay):

    def add_tabs(self) -> None:
        for name in [
                'source', 'event', 'actor', 'place', 'artifact', 'file',
                'type']:
            self.tabs[name] = Tab(name, entity=self.entity)
        for link_ in self.entity.get_links('P67'):
            range_ = link_.range
            data = get_base_table_data(range_)
            data.append(link_.description)
            data.append(
                edit_link(
                    url_for(
                        'link_update',
                        id_=link_.id,
                        origin_id=self.entity.id)))
            data.append(
                remove_link(
                    range_.name,
                    link_,
                    self.entity,
                    range_.class_.view))
            self.tabs[range_.class_.view].table.rows.append(data)


class TypeBaseDisplay(BaseDisplay):
    def add_crumbs(self) -> None:
        self.crumbs = [link(self.entity, index=True)]
        self.crumbs += [g.types[type_id] for type_id in self.entity.root]
        self.crumbs.append(self.entity.name)

    def add_button_copy(self) -> None:
        pass

    def add_button_delete(self) -> None:
        if self.entity.category != 'system':
            url = url_for('type_delete', id_=self.entity.id)
            if self.entity.count or self.entity.subs:
                url = url_for('type_delete_recursive', id_=self.entity.id)
            self.buttons.append(button(_('delete'), url))

    def add_button_others(self) -> None:
        if is_authorized('editor') and self.entity.category != 'value':
            if not self.entity.selectable:
                self.buttons.append(
                    button(
                        _('set selectable'),
                        url_for('type_set_selectable', id_=self.entity.id)))
            elif not self.entity.count:
                self.buttons.append(
                    button(
                        _('set unselectable'),
                        url_for('type_unset_selectable', id_=self.entity.id)))

    # def add_button_update(self) -> None:
    #    if self.entity.category != 'system':
    #        super().add_button_update()

    def add_data(self) -> None:
        self.data[_('super')] = link(g.types[self.entity.root[-1]])
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
        # self.add_reference_tables_data()
        for sub_id in entity.subs:
            self.tabs['subs'].table.rows.append([
                link(g.types[sub_id]),
                g.types[sub_id].count,
                g.types[sub_id].description])
        if entity.category == 'value':
            self.tabs['entities'].table.header = \
                [_('name'), _('value'), _('class'), _('info')]
        classes_ = [
            'feature',
            'stratigraphic_unit',
            'artifact',
            'human_remains']
        possible_sub_unit = False
        if any(item in g.types[entity.root[0]].classes for item in classes_):
            possible_sub_unit = True
            self.tabs['entities'].table.header.append('place')
        root = g.types[entity.root[0]] if entity.root else entity
        if root.name in app.config['PROPERTY_TYPES']:
            self.tabs['entities'].table.header = [_('domain'), _('range')]
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

    def get_chart_data(self) -> Optional[dict[str, Any]]:
        return get_chart_data(self.entity)
