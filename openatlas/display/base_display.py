from typing import Any, Optional, Union

from flask import g, render_template, url_for
from flask_babel import lazy_gettext as _
from flask_login import current_user

from openatlas import app
from openatlas.display.tab import Tab
from openatlas.display.util import edit_link, remove_link
from openatlas.models.entity import Entity
from openatlas.models.gis import Gis
from openatlas.models.link import Link
from openatlas.models.reference_system import ReferenceSystem
from openatlas.models.type import Type
from openatlas.models.user import User
from openatlas.util.util import (
    bookmark_toggle, button, display_delete_link, external_url, format_date,
    format_entity_date, get_appearance, get_base_table_data, get_system_data,
    get_type_data, is_authorized, link, manual, uc_first)


class BaseDisplay:

    entity: Union[Entity, Type]
    tabs: dict[str, Tab]
    event_links: Optional[list[Link]] = None  # Needed for actor and info data
    linked_places: list[Entity]  # Related places for map
    gis_data: dict[str, Any] = None
    structure = None
    overlays = None

    def __init__(self, entity: Union[Entity, Type]) -> None:
        self.entity = entity
        self.event_links = []
        self.linked_places = []
        self.add_tabs()
        self.add_info_content()  # Call later because of profile image
        self.entity.image_id = entity.get_profile_image_id()

    def add_tabs(self) -> None:
        self.tabs = {'info': Tab('info')}

    def add_info_content(self):
        self.entity.info_data = self.get_entity_data()
        problematic_type_id = self.entity.check_too_many_single_type_links()
        buttons = [manual(f'entity/{self.entity.class_.view}')]
        buttons += self.add_buttons(bool(problematic_type_id))
        buttons.append(bookmark_toggle(self.entity.id))
        # if not self.gis_data:
        #    self.gis_data = Gis.get_all(self.entity.linked_places) \
        #        if self.entity.linked_places else None
        # if self.entity.class_.view == 'file':
        #    if self.entity.image_id:
        #        buttons.append(download_button(self.entity))
        #    else:
        #        buttons.append(
        #            '<span class="error">' + uc_first(_("missing file")) +
        #            '</span>')
        # buttons.append(siblings_pager(self.entity, self.structure))
        self.tabs['info'].content = render_template(
            'entity/view.html',
            buttons=buttons,
            entity=self.entity,
            gis_data=self.gis_data,
            overlays=self.overlays,
            title=self.entity.name,
            problematic_type_id=problematic_type_id)

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

    def add_buttons(self, type_problem: bool = False) -> list[str]:
        if not is_authorized(self.entity.class_.write_access):
            return []  # pragma: no cover
        buttons = []
        if isinstance(self.entity, Type):
            if self.entity.root and self.entity.category != 'system':
                buttons.append(
                    button(_('edit'), url_for('update', id_=self.entity.id)))
                buttons.append(display_delete_link(self.entity))
        elif isinstance(self.entity, ReferenceSystem):
            buttons.append(
                button(_('edit'), url_for('update', id_=self.entity.id)))
            if not self.entity.classes and not self.entity.system:
                buttons.append(display_delete_link(self.entity))
        elif self.entity.class_.name == 'source_translation':
            buttons.append(
                button(_('edit'), url_for('update', id_=self.entity.id)))
            buttons.append(display_delete_link(self.entity))
        else:
            if not type_problem:
                buttons.append(
                    button(_('edit'), url_for('update', id_=self.entity.id)))
            if self.entity.class_.view != 'place' \
                    or not self.entity.get_linked_entities('P46'):
                buttons.append(display_delete_link(self.entity))
        if self.entity.class_.name == 'stratigraphic_unit':
            buttons.append(
                button(
                    _('tools'),
                    url_for('anthropology_index', id_=self.entity.id)))
        return buttons

    def get_profile_image_table_link(
            self,
            file: Entity,
            extension: str) -> str:
        if file.id == self.entity.image_id:
            return link(
                _('unset'),
                url_for('file_remove_profile_image', entity_id=self.entity.id))
        if extension in app.config['DISPLAY_FILE_EXTENSIONS'] or (
                g.settings['image_processing']
                and extension in app.config['ALLOWED_IMAGE_EXT']):
            return link(
                _('set'),
                url_for(
                    'set_profile_image',
                    id_=file.id,
                    origin_id=self.entity.id))
        return ''  # pragma: no cover

    def get_entity_data(self) -> dict[str, Any]:
        entity = self.entity
        data: dict[str, Any] = {_('alias'): list(entity.aliases.values())}

        # Dates
        from_link = ''
        to_link = ''
        if entity.class_.name == 'move':  # Add places to dates if it's a move
            if place_from := entity.get_linked_entity('P27'):
                from_link = \
                    link(place_from.get_linked_entity_safe('P53', True)) + ' '
            if place_to := entity.get_linked_entity('P26'):
                to_link = link(
                    place_to.get_linked_entity_safe('P53', True)) + ' '
        data[_('begin')] = from_link + format_entity_date(entity, 'begin')
        data[_('end')] = to_link + format_entity_date(entity, 'end')

        # Types
        if entity.standard_type:
            title = ' > '.join(
                [g.types[id_].name for id_ in entity.standard_type.root])
            data[_('type')] = \
                f'<span title="{title}">{link(entity.standard_type)}</span>'
        data.update(get_type_data(entity))

        # Class specific information
        from openatlas.models.type import Type
        from openatlas.models.reference_system import ReferenceSystem
        if isinstance(entity, Type):
            data[_('super')] = link(g.types[entity.root[-1]])
            if entity.category == 'value':
                data[_('unit')] = entity.description
            data[_('ID for imports')] = entity.id
        elif isinstance(entity, ReferenceSystem):
            data[_('website URL')] = external_url(entity.website_url)
            data[_('resolver URL')] = external_url(entity.resolver_url)
            data[_('example ID')] = entity.placeholder
        elif entity.class_.view == 'actor':
            begin_object = None
            if begin_place := entity.get_linked_entity('OA8'):
                begin_object = begin_place.get_linked_entity_safe('P53', True)
                self.linked_places.append(begin_object)
            end_object = None
            if end_place := entity.get_linked_entity('OA9'):
                end_object = end_place.get_linked_entity_safe('P53', True)
                self.linked_places.append(end_object)
            if residence := entity.get_linked_entity('P74'):
                residence_object =\
                    residence.get_linked_entity_safe('P53', True)
                self.linked_places.append(residence_object)
                data[_('residence')] = link(residence_object)
            data[_('alias')] = list(entity.aliases.values())
            data[_('begin')] = \
                format_entity_date(entity, 'begin', begin_object)
            data[_('end')] = format_entity_date(entity, 'end', end_object)
            if self.event_links:
                appears_first, appears_last = get_appearance(self.event_links)
                data[_('appears first')] = appears_first
                data[_('appears last')] = appears_last
        elif entity.class_.view == 'artifact':
            data[_('source')] = \
                [link(source) for source in entity.get_linked_entities('P128')]
            data[_('owned by')] = link(entity.get_linked_entity('P52'))
        elif entity.class_.view == 'event':
            data[_('sub event of')] = link(entity.get_linked_entity('P9'))
            data[_('preceding event')] = link(
                entity.get_linked_entity('P134', True))
            data[_('succeeding event')] = \
                '<br>'.join(
                    [link(e) for e in entity.get_linked_entities('P134')])
            if entity.class_.name == 'move':
                person_data = []
                artifact_data = []
                for linked_entity in entity.get_linked_entities('P25'):
                    if linked_entity.class_.name == 'person':
                        person_data.append(linked_entity)
                    elif linked_entity.class_.view == 'artifact':
                        artifact_data.append(linked_entity)
                data[_('person')] = [link(item) for item in person_data]
                data[_('artifact')] = [link(item) for item in artifact_data]
            else:
                if place := entity.get_linked_entity('P7'):
                    data[_('location')] = link(
                        place.get_linked_entity_safe('P53', True))
            if entity.class_.name == 'acquisition':
                data[_('recipient')] = \
                    [link(actor) for actor in
                     entity.get_linked_entities('P22')]
                data[_('donor')] = \
                    [link(donor) for donor in
                     entity.get_linked_entities('P23')]
                data[_('given place')] = []
                data[_('given artifact')] = []
                for item in entity.get_linked_entities('P24'):
                    label = _('given artifact') \
                        if item.class_.name == 'artifact' else _('given place')
                    data[label].append(link(item))
            if entity.class_.name == 'production':
                data[_('produced')] = \
                    [link(item) for item in entity.get_linked_entities('P108')]
        elif entity.class_.view == 'file':
            data[_('size')] = g.file_stats[entity.id]['size'] \
                if entity.id in g.file_stats else 'N/A'
            data[_('extension')] = g.file_stats[entity.id]['ext'] \
                if entity.id in g.file_stats else 'N/A'
        elif entity.class_.view == 'source':
            data[_('artifact')] = [
                link(artifact) for artifact in
                entity.get_linked_entities('P128', inverse=True)]
        if hasattr(current_user, 'settings'):
            data |= get_system_data(entity)
        if not self.gis_data and self.linked_places:
            self.gis_data = Gis.get_all(self.linked_places)
        self.add_note_tab()
        return data


class ActorDisplay(BaseDisplay):

    def add_tabs(self) -> None:
        super().add_tabs()
        for name in [
                'source', 'event', 'relation', 'member_of', 'member',
                'artifact', 'reference', 'file']:
            self.tabs[name] = Tab(name, entity=self.entity)
        self.event_links = \
            self.entity.get_links(['P11', 'P14', 'P22', 'P23', 'P25'], True)
        for link_ in self.event_links:
            event = link_.domain
            link_.object_ = None  # Needed for first/last appearance
            for place in event.get_linked_entities(['P7', 'P26', 'P27']):
                object_ = place.get_linked_entity_safe('P53', True)
                self.linked_places.append(object_)
                link_.object_ = object_
            first = link_.first
            if not link_.first and event.first:
                first = f'<span class="inactive">{event.first}</span>'
            last = link_.last
            if not link_.last and event.last:
                last = f'<span class="inactive">{event.last}</span>'
            data = [
                link(event),
                event.class_.label,
                _('moved')
                if link_.property.code == 'P25' else link(link_.type),
                first,
                last,
                link_.description]
            if link_.property.code == 'P25':
                data.append('')
            else:
                data.append(
                    edit_link(
                        url_for(
                            'link_update',
                            id_=link_.id,
                            origin_id=self.entity.id)))
            data.append(
                remove_link(link_.domain.name, link_, self.entity, 'event'))
            self.tabs['event'].table.rows.append(data)
        for link_ in self.entity.get_links('OA7') + \
                self.entity.get_links('OA7', True):
            type_ = ''
            if self.entity.id == link_.domain.id:
                related = link_.range
                if link_.type:
                    type_ = link(
                        link_.type.get_name_directed(),
                        url_for('view', id_=link_.type.id))
            else:
                related = link_.domain
                if link_.type:
                    type_ = link(
                        link_.type.get_name_directed(True),
                        url_for('view', id_=link_.type.id))
            self.tabs['relation'].table.rows.append([
                type_,
                link(related),
                link_.first,
                link_.last,
                link_.description,
                edit_link(
                    url_for(
                        'link_update',
                        id_=link_.id,
                        origin_id=self.entity.id)),
                remove_link(related.name, link_, self.entity, 'relation')])
        for link_ in self.entity.get_links('P107', True):
            data = [
                link(link_.domain),
                link(link_.type),
                link_.first,
                link_.last,
                link_.description,
                edit_link(
                    url_for(
                        'link_update',
                        id_=link_.id,
                        origin_id=self.entity.id)),
                remove_link(link_.domain.name, link_, self.entity, 'member-of')
            ]
            self.tabs['member_of'].table.rows.append(data)
        if self.entity.class_.name != 'group':
            del self.tabs['member']
        else:
            for link_ in self.entity.get_links('P107'):
                self.tabs['member'].table.rows.append([
                    link(link_.range),
                    link(link_.type),
                    link_.first,
                    link_.last,
                    link_.description,
                    edit_link(
                        url_for(
                            'link_update',
                            id_=link_.id,
                            origin_id=self.entity.id)),
                    remove_link(link_.range.name, link_, self.entity, 'member')
                ])
        for link_ in self.entity.get_links('P52', True):
            data = [
                link(link_.domain),
                link_.domain.class_.label,
                link(link_.domain.standard_type),
                link_.domain.first,
                link_.domain.last,
                link_.domain.description]
            self.tabs['artifact'].table.rows.append(data)
        for link_ in self.entity.get_links('P67', inverse=True):
            domain = link_.domain
            data = get_base_table_data(domain)
            if domain.class_.view == 'file':  # pragma: no cover
                extension = data[3]
                data.append(
                    self.get_profile_image_table_link(domain, extension))
                if not self.entity.image_id \
                        and extension in app.config['DISPLAY_FILE_EXTENSIONS']:
                    self.entity.image_id = domain.id
            if domain.class_.view not in ['source', 'file']:
                data.append(link_.description)
                data.append(edit_link(
                    url_for(
                        'link_update',
                        id_=link_.id,
                        origin_id=self.entity.id)))
                if domain.class_.view == 'reference_system':
                    self.entity.reference_systems.append(link_)
                    continue
            data.append(
                remove_link(
                    domain.name,
                    link_,
                    self.entity,
                    domain.class_.view))
            self.tabs[domain.class_.view].table.rows.append(data)


class EventsDisplay(BaseDisplay):

    def add_tabs(self) -> None:
        super().add_tabs()
        entity = self.entity
        for name in ['subs', 'source', 'actor', 'reference', 'file']:
            self.tabs[name] = Tab(name, entity=entity)
        for sub_event in entity.get_linked_entities(
                'P9',
                inverse=True,
                types=True):
            self.tabs['subs'].table.rows.append(get_base_table_data(sub_event))
        self.tabs['actor'].table.header.insert(5, _('activity'))
        for link_ in entity.get_links(['P11', 'P14', 'P22', 'P23']):
            first = link_.first
            if not link_.first and entity.first:
                first = f'<span class="inactive">{entity.first}</span>'
            last = link_.last
            if not link_.last and entity.last:
                last = f'<span class="inactive">{entity.last}</span>'
            self.tabs['actor'].table.rows.append([
                link(link_.range),
                link_.range.class_.label,
                link_.type.name if link_.type else '',
                first,
                last,
                g.properties[link_.property.code].name_inverse,
                link_.description,
                edit_link(
                    url_for('link_update', id_=link_.id, origin_id=entity.id)),
                remove_link(link_.range.name, link_, entity, 'actor')])
        entity.linked_places = [
            location.get_linked_entity_safe('P53', True) for location
            in entity.get_linked_entities(['P7', 'P26', 'P27'])]
        for link_ in entity.get_links('P67', inverse=True):
            domain = link_.domain
            data = get_base_table_data(domain)
            if domain.class_.view == 'file':  # pragma: no cover
                extension = data[3]
                data.append(
                    self.get_profile_image_table_link(domain, extension))
                if not entity.image_id \
                        and extension in app.config['DISPLAY_FILE_EXTENSIONS']:
                    entity.image_id = domain.id
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

class PlaceBaseDisplay(BaseDisplay):

    def add_tabs(self) -> None:
        super().add_tabs()
        entity = self.entity
        for name in ['source', 'event', 'reference', 'artifact']:
            self.tabs[name] = Tab(name, entity=entity)
        if self.entity.class_.name == 'place':
            self.tabs['actor'] = Tab('actor', entity=entity)
            self.tabs['feature'] = Tab('feature', entity=entity)
        elif self.entity.class_.name == 'feature':
            self.tabs['stratigraphic_unit'] =\
                Tab('stratigraphic_unit', entity=entity)
        self.tabs['file'] = Tab('file', entity=entity)
        if is_authorized('editor') \
                and current_user.settings['module_map_overlay']:
            self.tabs['file'].table.header.append(uc_first(_('overlay')))

        entity.location = entity.get_linked_entity_safe('P53', types=True)
        events = []  # Collect events to display actors
        event_ids = []  # Keep track of event ids to prevent event doubles
        for event in entity.location.get_linked_entities(
                ['P7', 'P24', 'P26', 'P27'],
                inverse=True):
            events.append(event)
            self.tabs['event'].table.rows.append(get_base_table_data(event))
            event_ids.append(event.id)
        for event in entity.get_linked_entities('P24', inverse=True):
            if event.id not in event_ids:  # Don't add again if already in table
                self.tabs['event'].table.rows.append(get_base_table_data(event))
                events.append(event)
        if entity.class_.name == 'place':
            for link_ in entity.location.get_links(
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
            for event in events:
                for actor in event.get_linked_entities(
                        ['P11', 'P14', 'P22', 'P23']):
                    if actor.id in actor_ids:
                        continue  # pragma: no cover
                    actor_ids.append(actor.id)
                    self.tabs['actor'].table.rows.append([
                        link(actor),
                        f"{_('participated at an event')}",
                        event.class_.name, '', '', ''])

    def add_info_content(self):
        super().add_info_content()
