from collections import defaultdict
from typing import Any, Optional, Union

from flask import g, render_template, url_for
from flask_babel import format_number, lazy_gettext as _
from flask_login import current_user

from openatlas import app
from openatlas.display.tab import Tab
from openatlas.display.util import (
    delete_link, edit_link, ext_references, format_entity_date, get_appearance,
    get_system_data, profile_image, profile_image_table_link, remove_link,
    siblings_pager)
from openatlas.models.entity import Entity
from openatlas.models.gis import Gis
from openatlas.models.link import Link
from openatlas.models.overlay import Overlay
from openatlas.models.reference_system import ReferenceSystem
from openatlas.models.type import Type
from openatlas.models.user import User
from openatlas.util.util import (
    bookmark_toggle, button, format_date, get_base_table_data, is_authorized,
    link, manual, uc_first)
from openatlas.views.entity_index import file_preview


class BaseDisplay:

    entity: Union[Entity, ReferenceSystem, Type]
    tabs: dict[str, Tab]
    events: Optional[list[Entity]]
    event_links: Optional[list[Link]]  # Needed for actor and info data
    linked_places: list[Entity]  # Related places for map
    gis_data: dict[str, Any] = None
    structure = None
    overlays = None
    crumbs: list[Any]
    buttons: list[str]
    problematic_type: bool = False
    data: dict[str, Any]

    def __init__(self, entity: Union[Entity, Type]) -> None:
        self.entity = entity
        self.events = []
        self.event_links = []
        self.linked_places = []
        self.problematic_type = self.entity.check_too_many_single_type_links()
        self.entity.image_id = entity.get_profile_image_id()
        self.add_tabs()
        self.add_note_tab()
        self.add_file_tab_thumbnails()
        self.add_crumbs()
        self.buttons = [manual(f'entity/{self.entity.class_.view}')]
        self.add_buttons()
        self.buttons.append(bookmark_toggle(self.entity.id))
        self.buttons.append(siblings_pager(self.entity, self.structure))
        if self.linked_places:
            self.gis_data = Gis.get_all(self.linked_places)
        self.add_info_tab_content()  # Call later because of profile image

    def add_tabs(self) -> None:
        self.tabs = {'info': Tab('info')}

    def add_crumbs(self) -> None:
        self.crumbs = [[
            _(self.entity.class_.view.replace('_', ' ')),
            url_for('index', view=self.entity.class_.view)]]
        if self.structure:
            for super_ in self.structure['supers']:
                self.crumbs.append(link(super_))
        self.crumbs.append(self.entity.name)

    def get_type_data(self) -> dict[str, Any]:
        if self.entity.location:  # Add location types
            self.entity.types.update(self.entity.location.types)
        data: dict[str, Any] = defaultdict(list)
        for type_, value in sorted(
                self.entity.types.items(),
                key=lambda x: x[0].name):
            if self.entity.standard_type and type_.id \
                    == self.entity.standard_type.id:
                continue  # Standard type is already added
            title = " > ".join([g.types[i].name for i in type_.root])
            html = f'<span title="{title}">{link(type_)}</span>'
            if type_.category == 'value':
                html += f' {float(value):g} {type_.description}'
            data[g.types[type_.root[0]].name].append(html)
        return {key: data[key] for key in sorted(data.keys())}

    def add_file_tab_thumbnails(self) -> None:
        if 'file' in self.tabs \
                and current_user.settings['table_show_icons'] \
                and g.settings['image_processing']:
            self.tabs['file'].table.header.insert(1, uc_first(_('icon')))
            for row in self.tabs['file'].table.rows:
                row.insert(1, file_preview(
                    int(row[0]
                        .replace('<a href="/entity/', '')
                        .split('"')[0])))

    def add_info_tab_content(self) -> None:
        self.add_data()
        if hasattr(current_user, 'settings'):
            self.data |= get_system_data(self.entity)
        self.tabs['info'].buttons = self.buttons
        self.tabs['info'].content = render_template(
            'entity/view.html',
            entity=self.entity,
            profile_image=profile_image(self.entity),
            info_data=self.data,
            gis_data=self.gis_data,
            overlays=self.overlays,
            ext_references=ext_references(self.entity.reference_systems),
            problematic_type_id=self.problematic_type)

    def add_note_tab(self) -> None:
        self.tabs['note'] = Tab('note', entity=self.entity)
        for note in current_user.get_notes_by_entity_id(self.entity.id):
            data = [
                format_date(note['created']),
                uc_first(_('public'))
                if note['public'] else uc_first(_('private')),
                link(User.get_by_id(note['user_id'])),
                note['text'],
                f'<a href="{url_for("note_view", id_=note["id"])}">' +
                uc_first(_("view")) + '</a>']
            self.tabs['note'].table.rows.append(data)

    def add_buttons(self) -> None:
        if is_authorized(self.entity.class_.write_access):
            if not self.problematic_type:
                self.buttons.append(
                    button(_('edit'), url_for('update', id_=self.entity.id)))
            self.buttons.append(delete_link(self.entity))

    def add_data(self) -> None:
        self.data = {
            _('alias'): list(self.entity.aliases.values()),
            _('begin'): format_entity_date(self.entity, 'begin'),
            _('end'): format_entity_date(self.entity, 'end')}
        if self.entity.standard_type:
            var = ' > '.join(
                [g.types[id_].name for id_ in self.entity.standard_type.root])
            self.data[_('type')] = \
                f'<span title="{var}">{link(self.entity.standard_type)}</span>'
        self.data.update(self.get_type_data())

    def add_reference_tables_data(self) -> None:
        entity = self.entity
        for link_ in entity.get_links('P67', inverse=True):
            domain = link_.domain
            data = get_base_table_data(domain)
            if domain.class_.view == 'file':
                extension = data[3]
                data.append(
                    profile_image_table_link(entity, domain, extension))
                if not entity.image_id \
                        and extension in app.config['DISPLAY_FILE_EXTENSIONS']:
                    entity.image_id = domain.id
            elif domain.class_.view != 'source':
                data.append(link_.description)
                data.append(edit_link(
                    url_for('link_update', id_=link_.id, origin_id=entity.id)))
                if domain.class_.view == 'reference_system':
                    entity.reference_systems.append(link_)
                    continue
            data.append(
                remove_link(domain.name, link_, entity, domain.class_.view))
            self.tabs[domain.class_.view].table.rows.append(data)


class ActorDisplay(BaseDisplay):

    def add_data(self) -> None:
        super().add_data()
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
        super().add_tabs()
        entity = self.entity
        for name in [
                'source', 'event', 'relation', 'member_of', 'member',
                'artifact', 'reference', 'file']:
            if entity.class_.name == 'group' or name != 'member':
                self.tabs[name] = Tab(name, entity=entity)
        self.add_reference_tables_data()
        self.event_links = \
            entity.get_links(['P11', 'P14', 'P22', 'P23', 'P25'], True)
        for link_ in self.event_links:
            event = link_.domain
            link_.object_ = None  # Needed for first/last appearance
            for place in event.get_linked_entities(['P7', 'P26', 'P27']):
                link_.object_ = place.get_linked_entity_safe('P53', True)
                self.linked_places.append(link_.object_)
            self.tabs['event'].table.rows.append([
                link(event),
                event.class_.label,
                _('moved')
                if link_.property.code == 'P25' else link(link_.type),
                link_.first or (
                    f'<span class="inactive">{event.first}</span>'
                    if event.first else ''),
                link_.last or (
                    f'<span class="inactive">{event.last}</span>'
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
        super().add_data()
        self.data[_('sub event of')] = \
            link(self.entity.get_linked_entity('P9'))
        self.data[_('preceding event')] = link(
            self.entity.get_linked_entity('P134', True))
        self.data[_('succeeding event')] = \
            '<br>'.join(
                [link(e) for e in self.entity.get_linked_entities('P134')])
        if place := self.entity.get_linked_entity('P7'):
            self.data[_('location')] = \
                link(place.get_linked_entity_safe('P53', True))

    def add_tabs(self) -> None:
        super().add_tabs()
        entity = self.entity
        for name in ['subs', 'source', 'actor', 'reference', 'file']:
            self.tabs[name] = Tab(name, entity=entity)
        self.add_reference_tables_data()
        for sub in entity.get_linked_entities('P9', inverse=True, types=True):
            self.tabs['subs'].table.rows.append(get_base_table_data(sub))
        self.tabs['actor'].table.header.insert(5, _('activity'))
        for link_ in entity.get_links(['P11', 'P14', 'P22', 'P23']):
            self.tabs['actor'].table.rows.append([
                link(link_.range),
                link_.range.class_.label,
                link_.type.name if link_.type else '',
                link_.first or f'<span class="inactive">{entity.first}</span>'
                if entity.first else '',
                link_.last or f'<span class="inactive">{entity.last}</span>'
                if entity.last else '',
                g.properties[link_.property.code].name_inverse,
                link_.description,
                edit_link(
                    url_for('link_update', id_=link_.id, origin_id=entity.id)),
                remove_link(link_.range.name, link_, entity, 'actor')])
        entity.linked_places = [
            location.get_linked_entity_safe('P53', True) for location
            in entity.get_linked_entities(['P7', 'P26', 'P27'])]


class PlaceBaseDisplay(BaseDisplay):

    def add_buttons(self) -> None:
        if is_authorized(self.entity.class_.write_access):
            if not self.problematic_type:
                self.buttons.append(
                    button(_('edit'), url_for('update', id_=self.entity.id)))
            if not self.entity.get_linked_entities('P46'):
                self.buttons.append(delete_link(self.entity))

    def add_tabs(self) -> None:
        super().add_tabs()
        entity = self.entity
        for name in ['source', 'event', 'reference', 'artifact']:
            self.tabs[name] = Tab(name, entity=entity)
        if entity.class_.name == 'place':
            self.tabs['actor'] = Tab('actor', entity=entity)
            self.tabs['feature'] = Tab('feature', entity=entity)
        elif entity.class_.name == 'feature':
            self.tabs['stratigraphic_unit'] = \
                Tab('stratigraphic_unit', entity=entity)
        self.tabs['file'] = Tab('file', entity=entity)
        if entity.class_.view == 'place' \
                and is_authorized('editor') \
                and current_user.settings['module_map_overlay']:
            self.tabs['file'].table.header.append(uc_first(_('overlay')))

        for link_ in entity.get_links('P67', inverse=True):
            domain = link_.domain
            data = get_base_table_data(domain)
            if domain.class_.view == 'file':
                extension = data[3]
                data.append(
                    profile_image_table_link(entity, domain, extension))
                if not entity.image_id \
                        and extension in app.config['DISPLAY_FILE_EXTENSIONS']:
                    entity.image_id = domain.id
                if entity.class_.view == 'place' \
                        and is_authorized('editor') \
                        and current_user.settings['module_map_overlay']:
                    content = ''
                    if extension in app.config['DISPLAY_FILE_EXTENSIONS']:
                        overlays = Overlay.get_by_object(entity)
                        if domain.id in overlays:
                            content = edit_link(
                                url_for(
                                    'overlay_update',
                                    id_=overlays[domain.id].id))
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
                if domain.class_.view == 'reference_system':
                    entity.reference_systems.append(link_)
                    continue
            data.append(
                remove_link(domain.name, link_, entity, domain.class_.view))
            self.tabs[domain.class_.view].table.rows.append(data)

        entity.location = entity.get_linked_entity_safe('P53', types=True)
        event_ids = []  # Keep track of event ids to prevent event doubles
        for event in \
                entity.get_linked_entities(['P24', 'P25', 'P108'], True) + \
                entity.location.get_linked_entities(
                    ['P7', 'P26', 'P27'],
                    True):
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
        super().add_tabs()
        for name in [
                'source', 'event', 'actor', 'place', 'feature',
                'stratigraphic_unit', 'artifact', 'file']:
            self.tabs[name] = Tab(name, entity=self.entity)
        for link_ in self.entity.get_links('P67'):
            range_ = link_.range
            data = get_base_table_data(range_)
            data.append(link_.description)
            data.append(edit_link(url_for(
                'link_update',
                id_=link_.id,
                origin_id=self.entity.id)))
            data.append(remove_link(
                range_.name,
                link_,
                self.entity,
                range_.class_.name))
            self.tabs[range_.class_.view].table.rows.append(data)


class TypeBaseDisplay(BaseDisplay):

    def add_data(self) -> None:
        super().add_data()
        self.data[_('super')] = link(g.types[self.entity.root[-1]])
        if self.entity.category == 'value':
            self.data[_('unit')] = self.entity.description
        self.data[_('ID for imports')] = self.entity.id

    def add_buttons(self) -> None:
        if is_authorized(self.entity.class_.write_access) \
                and self.entity.root and self.entity.category != 'system':
            self.buttons.append(
                button(_('edit'), url_for('update', id_=self.entity.id)))
            self.buttons.append(delete_link(self.entity))

    def add_crumbs(self) -> None:
        self.crumbs = [[_('types'), url_for('type_index')]]
        self.crumbs += [g.types[type_id] for type_id in self.entity.root]
        self.crumbs.append(self.entity.name)

    def add_tabs(self) -> None:
        super().add_tabs()
        entity = self.entity
        self.tabs['subs'] = Tab('subs', entity=entity)
        self.tabs['entities'] = Tab('entities', entity=entity)
        self.tabs['file'] = Tab('file', entity=entity)
        self.add_reference_tables_data()
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
        if any(item in g.types[entity.root[0]].classes for item in classes_):
            self.tabs['entities'].table.header.append('place')
        root = g.types[entity.root[0]] if entity.root else entity
        if root.name in app.config['PROPERTY_TYPES']:
            self.tabs['entities'].table.header = [_('domain'), _('range')]
            for row in Link.get_links_by_type(entity):
                self.tabs['entities'].table.rows.append([
                    link(Entity.get_by_id(row['domain_id'])),
                    link(Entity.get_by_id(row['range_id']))])
        else:
            for item in entity.get_linked_entities(['P2', 'P89'], True, True):
                if item.class_.name == 'object_location':
                    item = item.get_linked_entity_safe('P53', inverse=True)
                data = [link(item)]
                if entity.category == 'value':
                    data.append(format_number(item.types[entity]))
                data.append(item.class_.label)
                data.append(item.description)
                root_place = ''
                if item.class_.name in classes_:
                    if roots := \
                            item.get_linked_entities_recursive('P46', True):
                        root_place = link(roots[0])
                data.append(root_place)
                self.tabs['entities'].table.rows.append(data)
