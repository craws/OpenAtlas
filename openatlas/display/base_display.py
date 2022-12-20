from collections import defaultdict
from typing import Any, Optional, Union

from flask import g, render_template, url_for
from flask_babel import format_number, lazy_gettext as _
from flask_login import current_user

from openatlas import app
from openatlas.display.tab import Tab
from openatlas.display.util import (
    edit_link, ext_references, format_entity_date, get_appearance, remove_link)
from openatlas.models.entity import Entity
from openatlas.models.gis import Gis
from openatlas.models.link import Link
from openatlas.models.overlay import Overlay
from openatlas.models.reference_system import ReferenceSystem
from openatlas.models.type import Type
from openatlas.models.user import User
from openatlas.util.util import (
    bookmark_toggle, button, format_date, get_base_table_data, get_file_path,
    is_authorized, link, manual, uc_first)
from openatlas.views.entity_index import file_preview


class BaseDisplay:

    entity: Union[Entity, ReferenceSystem, Type]
    tabs: dict[str, Tab]
    events: Optional[list[Entity]]
    event_links: Optional[list[Link]] = None  # Needed for actor and info data
    linked_places: list[Entity]  # Related places for map
    gis_data: dict[str, Any] = None
    structure = None
    overlays = None
    crumbs = None
    buttons = None
    problematic_type: bool = False

    def __init__(self, entity: Union[Entity, Type]) -> None:
        self.entity = entity
        self.events = []
        self.event_links = []
        self.linked_places = []
        self.problematic_type = self.entity.check_too_many_single_type_links()
        self.add_tabs()
        self.add_crumbs()
        self.add_buttons()
        self.add_info_content()  # Call later because of profile image
        self.entity.image_id = entity.get_profile_image_id()

    def add_tabs(self) -> None:
        self.tabs = {'info': Tab('info')}

    def add_crumbs(self) -> None:
        self.crumbs = [[
            _(self.entity.class_.view.replace('_', ' ')),
            url_for('index', view=self.entity.class_.view)]]
        if self.structure:
            for super_ in self.structure['supers']:
                self.crumbs.append(link(super_))
        elif isinstance(self.entity, Type):
            self.crumbs = [[_('types'), url_for('type_index')]]
            if self.entity.root:
                self.crumbs += \
                    [g.types[type_id] for type_id in self.entity.root]
        elif self.entity.class_.view == 'source_translation':
            self.crumbs = [
                [_('source'), url_for('index', view='source')],
                self.entity.get_linked_entity('P73', True)]
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

    def add_info_content(self):
        if self.linked_places and not self.gis_data:
            self.gis_data = Gis.get_all(self.linked_places)
        if 'file' in self.tabs \
                and current_user.settings['table_show_icons'] \
                and g.settings['image_processing']:
            self.tabs['file'].table.header.insert(1, uc_first(_('icon')))
            for row in self.tabs['file'].table.rows:
                row.insert(
                    1,
                    file_preview(
                        int(
                            row[0].
                            replace('<a href="/entity/', '').split('"')[0])))
        self.tabs['info'].content = render_template(
            'entity/view.html',
            buttons=self.buttons,
            entity=self.entity,
            info_data=self.get_entity_data(),
            gis_data=self.gis_data,
            overlays=self.overlays,
            title=self.entity.name,
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
        self.buttons = [manual(f'entity/{self.entity.class_.view}')]
        if not is_authorized(self.entity.class_.write_access):
            return  # pragma: no cover
        if isinstance(self.entity, Type):
            if self.entity.root and self.entity.category != 'system':
                self.buttons.append(
                    button(_('edit'), url_for('update', id_=self.entity.id)))
                self.buttons.append(self.display_delete_link())
        elif isinstance(self.entity, ReferenceSystem):
            self.buttons.append(
                button(_('edit'), url_for('update', id_=self.entity.id)))
            if not self.entity.classes and not self.entity.system:
                self.buttons.append(self.display_delete_link())
        elif self.entity.class_.name == 'source_translation':
            self.buttons.append(
                button(_('edit'), url_for('update', id_=self.entity.id)))
            self.buttons.append(self.display_delete_link())
        else:
            if not self.problematic_type:
                self.buttons.append(
                    button(_('edit'), url_for('update', id_=self.entity.id)))
            if self.entity.class_.view != 'place' \
                    or not self.entity.get_linked_entities('P46'):
                self.buttons.append(self.display_delete_link())
        if self.entity.class_.name == 'stratigraphic_unit':
            self.buttons.append(
                button(
                    _('tools'),
                    url_for('anthropology_index', id_=self.entity.id)))
        if self.entity.class_.view == 'file':
            if path := get_file_path(self.entity.id):
                self.buttons.append(
                    button(
                        _('download'),
                        url_for('download_file', filename=path.name)))
            else:
                self.buttons.append(
                    '<span class="error">' + uc_first(_("missing file")) +
                    '</span>')
        self.buttons.append(bookmark_toggle(self.entity.id))
        self.buttons.append(self.siblings_pager())

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

    def siblings_pager(self) -> str:
        if not self.structure or len(self.structure['siblings']) < 2:
            return ''
        self.structure['siblings'].sort(key=lambda x: x.id)
        prev_id = None
        next_id = None
        position = None
        for counter, sibling in enumerate(self.structure['siblings']):
            position = counter + 1
            prev_id = sibling.id if sibling.id < self.entity.id else prev_id
            if sibling.id > self.entity.id:
                next_id = sibling.id
                position = counter
                break
        parts = []
        if prev_id:  # pragma: no cover
            parts.append(button('<', url_for('view', id_=prev_id)))
        if next_id:
            parts.append(button('>', url_for('view', id_=next_id)))
        parts.append(f"{position} {_('of')} {len(self.structure['siblings'])}")
        return ' '.join(parts)

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
        data.update(self.get_type_data())

        # Class specific information
        from openatlas.models.type import Type
        from openatlas.models.reference_system import ReferenceSystem
        if isinstance(entity, Type):
            data[_('super')] = link(g.types[entity.root[-1]])
            if entity.category == 'value':
                data[_('unit')] = entity.description
            data[_('ID for imports')] = entity.id
        elif isinstance(entity, ReferenceSystem):
            data[_('website URL')] = \
                link(entity.website_url, entity.website_url, external=True)
            data[_('resolver URL')] = \
                link(entity.resolver_url, entity.resolver_url, external=True)
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
            data |= self.get_system_data()
        self.add_note_tab()
        return data

    def get_system_data(self) -> dict[str, Any]:
        data = {}
        if 'entity_show_class' in current_user.settings \
                and current_user.settings['entity_show_class']:
            data[_('class')] = link(self.entity.cidoc_class)
        info = g.logger.get_log_info(self.entity.id)
        if 'entity_show_dates' in current_user.settings \
                and current_user.settings['entity_show_dates']:
            data[_('created')] = \
                f"{format_date(self.entity.created)} {link(info['creator'])}"
            if info['modified']:
                data[_('modified')] = \
                    f"{format_date(info['modified'])} {link(info['modifier'])}"
        if 'entity_show_import' in current_user.settings \
                and current_user.settings['entity_show_import']:
            data[_('imported from')] = link(info['project'])
            data[_('imported by')] = link(info['importer'])
            data['origin ID'] = info['origin_id']
        if 'entity_show_api' in current_user.settings \
                and current_user.settings['entity_show_api']:
            data['API'] = \
                render_template('util/api_links.html', entity=self.entity)
        return data

    def display_delete_link(self) -> str:
        entity = self.entity
        confirm = ''
        if isinstance(entity, Type):
            url = url_for('type_delete', id_=entity.id)
            if entity.count or entity.subs:
                url = url_for('type_delete_recursive', id_=entity.id)
        else:
            if current_user.group == 'contributor':  # pragma: no cover
                info = g.logger.get_log_info(entity.id)
                if not info['creator'] \
                        or info['creator'].id != current_user.id:
                    return ''
            url = url_for(
                'index',
                view=entity.class_.view,
                delete_id=entity.id)
            confirm = _('Delete %(name)s?', name=entity.name.replace('\'', ''))
        return button(
            _('delete'),
            url,
            onclick=f"return confirm('{confirm}')" if confirm else '')


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
                if domain.class_.view \
                        == 'reference_system':  # pragma: no cover
                    entity.reference_systems.append(link_)
                    continue
            data.append(
                remove_link(domain.name, link_, entity, domain.class_.view))
            self.tabs[domain.class_.view].table.rows.append(data)


class PlaceBaseDisplay(BaseDisplay):

    def add_info_content(self):
        super().add_info_content()

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
                if entity.class_.view == 'place' \
                        and is_authorized('editor') \
                        and current_user.settings['module_map_overlay']:
                    overlays = Overlay.get_by_object(entity)
                    if extension in app.config['DISPLAY_FILE_EXTENSIONS']:
                        if domain.id in overlays:
                            data.append(edit_link(
                                url_for(
                                    'overlay_update',
                                    id_=overlays[domain.id].id)))
                        else:
                            data.append(link(_('link'), url_for(
                                'overlay_insert',
                                image_id=domain.id,
                                place_id=entity.id,
                                link_id=link_.id)))
                    else:  # pragma: no cover
                        data.append('')
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
        for event in entity.location.get_linked_entities(
                ['P7', 'P24', 'P26', 'P27'],
                inverse=True):
            self.events.append(event)
            self.tabs['event'].table.rows.append(get_base_table_data(event))
            event_ids.append(event.id)
        for event in entity.get_linked_entities('P24', inverse=True):
            if event.id not in event_ids:  # Don't add again
                self.tabs['event'].table.rows.append(
                    get_base_table_data(event))
                self.events.append(event)
        if structure := entity.get_structure():
            self.structure = structure
            for item in structure['subunits']:
                name = 'artifact' if item.class_.view == 'artifact' \
                    else item.class_.name
                self.tabs[name].table.rows.append(get_base_table_data(item))
        self.gis_data = Gis.get_all([entity], structure)
        if self.gis_data['gisPointSelected'] == '[]' \
                and self.gis_data['gisPolygonSelected'] == '[]' \
                and self.gis_data['gisLineSelected'] == '[]' \
                and (not structure or not structure['supers']):
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
                    range_.class_.name))
            self.tabs[range_.class_.view].table.rows.append(data)


class TypeBaseDisplay(BaseDisplay):

    def add_tabs(self) -> None:
        super().add_tabs()
        self.tabs['subs'] = Tab('subs', entity=self.entity)
        self.tabs['entities'] = Tab('entities', entity=self.entity)
        self.tabs['file'] = Tab('file', entity=self.entity)
        for sub_id in self.entity.subs:
            sub = g.types[sub_id]
            self.tabs['subs'].table.rows.append([
                link(sub),
                sub.count,
                sub.description])
        if self.entity.category == 'value':
            self.tabs['entities'].table.header = \
                [_('name'), _('value'), _('class'), _('info')]
        place_classes = [
            'feature',
            'stratigraphic_unit',
            'artifact',
            'human_remains']
        if any(item in g.types[self.entity.root[0]].classes for item in
               place_classes):
            self.tabs['entities'].table.header.append('place')
        root = g.types[self.entity.root[0]] if self.entity.root \
            else self.entity
        if root.name in app.config['PROPERTY_TYPES']:
            self.tabs['entities'].table.header = [_('domain'), _('range')]
            for row in Link.get_links_by_type(self.entity):
                self.tabs['entities'].table.rows.append([
                    link(Entity.get_by_id(row['domain_id'])),
                    link(Entity.get_by_id(row['range_id']))])
        else:
            for item in self.entity.get_linked_entities(
                    ['P2', 'P89'],
                    inverse=True,
                    types=True):
                if item.class_.name in ['location', 'reference_system']:
                    continue  # pragma: no cover
                if item.class_.name == 'object_location':
                    item = item.get_linked_entity_safe('P53', inverse=True)
                data = [link(item)]
                if self.entity.category == 'value':
                    data.append(format_number(item.types[self.entity]))
                data.append(item.class_.label)
                data.append(item.description)
                root_place = ''
                if item.class_.name in place_classes:
                    if roots := item.get_linked_entities_recursive(
                            'P46',
                            True):
                        root_place = link(roots[0])
                data.append(root_place)
                self.tabs['entities'].table.rows.append(data)

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
            if domain.class_.view \
                    not in ['source', 'file']:  # pragma: no cover
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
