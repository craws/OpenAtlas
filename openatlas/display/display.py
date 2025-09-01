from collections import defaultdict
from typing import Any, Optional

from flask import g, render_template, url_for
from flask_babel import lazy_gettext as _
from flask_login import current_user
from markupsafe import escape

from openatlas.display.tab import Tab
from openatlas.display.table import entity_table
from openatlas.display.util import (
    bookmark_toggle, button, description, display_annotation_text_links,
    get_system_data, link, reference_systems)
from openatlas.display.util2 import (
    is_authorized, manual, show_table_icons, uc_first)
from openatlas.models.dates import format_date, format_entity_date
from openatlas.models.entity import Entity, Link
from openatlas.models.gis import Gis
from openatlas.models.user import User
from openatlas.views.entity_index import file_preview


class Display:
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
        self.add_tabs()
        if 'file' in self.tabs and show_table_icons():
            self.add_file_tab_thumbnails()
        self.add_crumbs()
        self.add_buttons()
        self.add_info_tab_content()  # Call later because of profile image

    def add_crumbs(self) -> None:
        self.crumbs = [link(self.entity, index=True)]
        if self.entity.class_.name == 'source_translation':
            self.crumbs = [
                [_('source'), url_for('index', view='source')],
                self.entity.get_linked_entity_safe('P73', True)]
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
            if self.entity.standard_type \
                    and type_.id == self.entity.standard_type.id:
                continue  # Standard type is already included
            title = " > ".join([g.types[i].name for i in type_.root])
            html = f'<span title="{title}">{link(type_)}</span>'
            if type_.category == 'value':
                html += f" {float(value):g} {type_.description or ''}"
            data[g.types[type_.root[0]].name].append(html)
        return {key: data[key] for key in sorted(data.keys())}

    def add_file_tab_thumbnails(self) -> None:
        self.tabs['file'].table.columns.insert(1, _('icon'))
        for row in self.tabs['file'].table.rows:
            id_ = int(row[0].replace('<a href="/entity/', '').split('"')[0])
            row.insert(1, file_preview(id_))

    def add_info_tab_content(self) -> None:
        self.add_data()
        if self.linked_places:
            self.gis_data = Gis.get_all(self.linked_places)
        resolver_url = g.settings['frontend_resolver_url']
        if hasattr(current_user, 'settings'):
            self.data |= get_system_data(self.entity)
            resolver_url = current_user.settings['frontend_resolver_url']
        self.tabs['info'].buttons = self.buttons
        frontend_link = None
        if resolver_url:
            frontend_link = link(
                '<i class="fas fa-eye"></i> ' +
                uc_first(_('presentation site')),
                resolver_url + str(self.entity.id),
                external=True)
        description_ = self.entity.description
        description_label = ''
        if 'description' in self.entity.class_.attributes and description_:
            if 'label' in self.entity.class_.attributes['description']:
                description_label = \
                    self.entity.class_.attributes['description']['label']
            if 'annotated' in self.entity.class_.attributes['description'] \
                    and self.entity.class_.attributes['description']:
                description_ = display_annotation_text_links(self.entity)
        self.tabs['info'].content = render_template(
            'entity/view.html',
            entity=self.entity,
            frontend_link=frontend_link,
            info_data=self.data,
            gis_data=self.gis_data,
            overlays=self.overlays,
            # chart_data=self.get_chart_data(),
            reference_systems=reference_systems(
                self.entity.get_links(
                    'P67',
                    ['reference_system'],
                    inverse=True)),
            description_html=description(description_, description_label),
            problematic_type_id=self.problematic_type)

    # def get_chart_data(self) -> Optional[dict[str, Any]]:
    #    return None

    def add_tabs(self) -> None:
        self.tabs = {'info': Tab('info')}
        for name, relation in self.entity.class_.relations.items():
            if not relation['tab']:
                continue
            items = []
            for item in self.entity.get_links(
                    relation['properties'],
                    relation['classes'],
                    relation['inverse']):
                items.append(item)
                if relation['properties'] == ['P67'] \
                        and relation['classes'] == ['file'] \
                        and not self.entity.image_id \
                        and item.domain.get_file_ext() in \
                        g.display_file_ext:
                    self.entity.image_id = \
                        self.entity.image_id or item.domain.id
            buttons = [manual(f'entity/{name}')]
            if is_authorized('contributor'):
                if 'link' in relation['tab']['buttons']:
                    buttons.append(
                        button(
                            _('link'),
                            url_for(
                                'link_insert_detail'
                                if relation['additional_fields']
                                else 'link_insert',
                                origin_id=self.entity.id,
                                relation_name=name)))
                if 'insert' in relation['tab']['buttons']:
                    for class_ in relation['classes']:
                        buttons.append(
                            button(
                                g.classes[class_].label,
                                url_for(
                                    'insert',
                                    class_=class_,
                                    origin_id=self.entity.id,
                                    relation=name)))
                #     case 'source':
                #         if class_name == 'file':
                #             self.buttons.append(
                #                 button(
                #                     _('link'),
                #                     url_for('file_add', id_=id_, view=tab_name)))
                #         elif view == 'reference':
                #             self.buttons.append(
                #                 button(
                #                     'link',
                #                     url_for('reference_add', id_=id_, view=tab_name)))
                #         self.buttons.append(
                #             button(
                #                 g.classes['source'].label,
                #                 url_for('insert', class_=tab_name, origin_id=id_)))
            self.tabs[name] = Tab(
                name,
                relation['label'],
                table=entity_table(
                    items,
                    self.entity,
                    relation['tab']['columns'],
                    relation['tab']['additional_columns'],
                    relation),
                buttons=buttons,
                entity=self.entity,
                tooltip=relation['tab']['tooltip'])

        for name in self.entity.class_.display['additional_tabs']:
            if name == 'note':
                self.add_note_tab()
                continue

    def add_note_tab(self) -> None:
        self.tabs['note'] = Tab(
            'note',
            buttons=[manual('tools/notes')],
            entity=self.entity)
        for note in current_user.get_notes_by_entity_id(self.entity.id):
            data = [
                format_date(note['created']),
                _('public') if note['public'] else _('private'),
                link(User.get_by_id(note['user_id'])),
                note['text'],
                link(_('view'), url_for('note_view', id_=note['id']))]
            self.tabs['note'].table.rows.append(data)

    def add_buttons(self) -> None:
        self.buttons = [manual(f"entity/{self.entity.class_.group['name']}")]
        if self.entity.class_.name == 'source_translation':
            self.buttons = [manual('entity/source')]
        if is_authorized(self.entity.class_.write_access):
            if not self.problematic_type:
                self.add_button_update()
                self.add_button_copy()
            self.add_button_delete()
        self.buttons.append(bookmark_toggle(self.entity.id))
        if 'network' in self.entity.class_.display['buttons']:
            self.buttons.append(
                button(
                    _('network'),
                    url_for('network', dimensions=0, id_=self.entity.id)))
        self.buttons.append(
            render_template('util/api_links.html', entity=self.entity))
        if self.structure and len(self.structure['siblings']) > 1:
            self.add_button_sibling_pager()

    def add_button_copy(self) -> None:
        if 'copy' in self.entity.class_.display['buttons']:
            self.buttons.append(
                button(
                    _('copy'),
                    url_for('update', id_=self.entity.id, copy='copy_')))

    def add_button_delete(self) -> None:
        if current_user.group == 'contributor':
            info = g.logger.get_log_info(self.entity.id)
            if not info['creator'] or info['creator'].id != current_user.id:
                return
        msg = _(
            'Delete %(name)s?',
            name=escape(self.entity.name.replace('\'', '')))
        self.buttons.append(button(
            _('delete'),
            url_for('delete', id_=self.entity.id),
            onclick=f"return confirm('{msg}')"))

    def add_button_update(self) -> None:
        self.buttons.append(
            button(_('edit'), url_for('update', id_=self.entity.id)))

    def add_button_sibling_pager(self) -> None:
        prev_id = None
        next_id = None
        position = None
        self.structure['siblings'].sort(key=lambda x: x.id)
        for counter, sibling in enumerate(self.structure['siblings']):
            position = counter + 1
            prev_id = sibling.id if sibling.id < self.entity.id else prev_id
            if sibling.id > self.entity.id:
                next_id = sibling.id
                position = counter
                break
        if prev_id:
            self.buttons.append(button('<', url_for('view', id_=prev_id)))
        if next_id:
            self.buttons.append(button('>', url_for('view', id_=next_id)))
        self.buttons.append(
            f'{position} ' + _('of') + f" {len(self.structure['siblings'])}")

    def add_data(self) -> None:
        self.data = {
            _('alias'): list(self.entity.aliases.values()),
            _('begin'): format_entity_date(self.entity.dates, 'begin'),
            _('end'): format_entity_date(self.entity.dates, 'end')}
        if self.entity.standard_type:
            var = ' > '.join(
                [g.types[id_].name for id_ in self.entity.standard_type.root])
            self.data[_('type')] = \
                f'<span title="{var}">{link(self.entity.standard_type)}</span>'
        self.data.update(self.get_type_data())
        for name, relation in self.entity.class_.relations.items():
            if relation['mode'] in ['direct', 'display']:
                self.data[relation['label']] = []
                for e in self.entity.get_linked_entities(
                        relation['properties'],
                        relation['classes'],
                        relation['inverse']):
                    if e.class_.name == 'object_location':
                        e = e.get_linked_entity_safe('P53', True)
                        self.linked_places.append(e)
                    if name == 'place_from':
                        self.data['begin'] = \
                            format_entity_date(self.entity.dates, 'begin', e)
                    elif name == 'place_to':
                        self.data['end'] = \
                            format_entity_date(self.entity.dates, 'end', e)
                    else:
                        self.data[relation['label']].append(link(e))
