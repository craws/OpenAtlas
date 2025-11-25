from collections import defaultdict
from typing import Any

from flask import g, render_template, url_for
from flask_babel import lazy_gettext as _
from flask_login import current_user
from markupsafe import escape

from openatlas import app
from openatlas.display.tab import Tab
from openatlas.display.table import entity_table
from openatlas.display.util import (
    bookmark_toggle, button, button_bar, description,
    display_annotation_text_links, format_entity_date, get_appearance,
    get_chart_data, get_file_path, get_system_data, link, reference_systems)
from openatlas.display.util2 import (
    display_bool, is_authorized, manual, uc_first)
from openatlas.models.dates import format_date
from openatlas.models.entity import Entity, Link
from openatlas.models.gis import Gis
from openatlas.models.user import User
from openatlas.views.tools import carbon_result, sex_result


class Display:
    buttons: list[str]
    data: dict[str, Any]
    tabs: dict[str, Tab]

    def __init__(self, entity: Entity) -> None:
        self.entity = entity
        self.events: list[Entity] = []
        self.linked_places: list[Entity] = []
        self.structure: dict[str, list[Entity]] = {}
        self.gis_data: dict[str, Any] = {}
        self.problematic_type = self.entity.check_too_many_single_type_links()
        self.entity.image_id = entity.get_profile_image_id()
        self.add_tabs()
        self.add_buttons()
        self.add_info_tab_content()
        if len(self.structure.get('siblings', [])) > 1:
            self.add_button_sibling_pager()

    def get_type_data(self) -> dict[str, Any]:
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

    def add_info_tab_content(self) -> None:
        self.add_data()
        if self.entity.class_.attributes.get('location'):
            self.structure = self.entity.get_structure()
            self.gis_data = Gis.get_all([self.entity], self.structure)
        elif self.linked_places:
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
        text = ''
        if 'stratigraphic_tools' in self.entity.class_.display['buttons']:
            if radiocarbon := carbon_result(self.entity):
                text += f"<p>{radiocarbon}</p>"
            if sex_estimation := sex_result(self.entity):
                text += f"<p>{sex_estimation}</p>"
        description_ = self.entity.description
        label = ''
        if 'description' in self.entity.class_.attributes and description_:
            if 'label' in self.entity.class_.attributes['description']:
                label = self.entity.class_.attributes['description']['label']
            if 'annotated' in self.entity.class_.attributes['description'] \
                    and self.entity.class_.attributes['description']:
                description_ = display_annotation_text_links(self.entity)
        if self.entity.category != 'value':
            text += description(description_, label)

        reference_systems_display = reference_systems(self.entity)
        self.tabs['info'].content = render_template(
            'entity/view.html',
            entity=self.entity,
            frontend_link=frontend_link,
            info_data=self.data,
            gis_data=self.gis_data,
            chart_data=get_chart_data(self.entity),
            reference_systems=reference_systems_display,
            description_html=text,
            problematic_type=self.problematic_type)

    def add_tabs(self) -> None:
        self.tabs = {'info': Tab('info')}

        for name, relation in self.entity.class_.relations.items():
            if not relation.mode == 'tab':
                continue
            entity_for_links = self.entity
            if self.entity.class_.name == 'place' \
                    and relation.reverse_relation \
                    and relation.reverse_relation.classes \
                    == ['object_location']:
                entity_for_links = self.entity.location
            items = []
            for item in entity_for_links.get_links(
                    relation.property,
                    relation.classes,
                    relation.inverse):
                if item.domain.class_.name == 'object_location':
                    item.domain = item.domain.get_linked_entity_safe(
                        'P53',
                        inverse=True,
                        types=True)
                items.append(item)
            if relation.name == 'relative':
                for item in entity_for_links.get_links(
                        relation.property,
                        relation.classes,
                        not relation.inverse):
                    item.range = item.domain
                    items.append(item)
            buttons = []
            if is_authorized('contributor'):
                for button_name in relation.tab['buttons']:
                    match button_name:
                        case 'link':
                            buttons.append(
                                button(
                                    _('link'),
                                    url_for(
                                        'link_insert_detail'
                                        if relation.additional_fields
                                        else 'link_insert',
                                        origin_id=self.entity.id,
                                        name=name)))
                        case 'insert':
                            for class_ in relation.classes:
                                buttons.append(
                                    button(
                                        g.classes[class_].label,
                                        url_for(
                                            'insert',
                                            class_=class_,
                                            origin_id=self.entity.id,
                                            relation=name),
                                        tooltip_text=g.classes[class_].
                                        display['tooltip']))
                        case 'move' if items:
                            root = g.types[self.entity.root[0]]
                            if root.category not in ['system', 'value']:
                                buttons.append(
                                    button(
                                        _('move entities'),
                                        url_for(
                                            'type_move_entities',
                                            id_=self.entity.id)))
                        case 'remove_reference_system_class' if not items \
                                and is_authorized('manager'):
                            buttons.append(
                                button(
                                    _('remove'),
                                    url_for(
                                        'reference_system_remove_class',
                                        system_id=self.entity.id,
                                        name=name)))
                        case 'show_all_iiif':
                            buttons.append(
                                button(
                                    _('view all IIIF images'),
                                    url_for('view_iiif', id_=self.entity.id)))
            if relation.classes:
                group = g.classes[relation.classes[0]].group.get('name')
                if buttons and group and (link_ := manual(f'entity/{group}')):
                    buttons.insert(0, link_)
            columns = relation.tab['columns']
            if self.entity.category == 'value' and relation.name == 'entities':
                columns = ['name', 'value', 'class', 'description']
            if self.entity.root and g.types[self.entity.root[0]].name \
                    in app.config['PROPERTY_TYPES']:
                columns = ['domain', 'range']
                items = [
                    Link.get_by_id(row['id']) for row in
                    Link.get_links_by_type(self.entity)]
            self.tabs[name] = Tab(
                name,
                relation.label,
                table=entity_table(
                    items,
                    self.entity,
                    columns,
                    relation.tab['additional_columns'] if relation else [],
                    relation),
                buttons=buttons,
                entity=self.entity,
                tooltip=relation.tab['tooltip'])

        for name in self.entity.class_.display['additional_tabs']:
            if name == 'note':
                self.add_note_tab()
                continue

        empty_tabs = []
        for name, tab in self.tabs.items():
            if name != 'info' and not tab.table.rows:
                empty_tabs.append(name)
        if empty_tabs:
            self.tabs['additional'] = Tab(
                'additional',
                '+ ' + uc_first(_('relation')),
                '')
            for name in empty_tabs:
                if self.tabs[name].buttons:
                    self.tabs['additional'].content += \
                        f"<h2>{self.tabs[name].label}</h2>" + \
                        button_bar(self.tabs[name].buttons)
                del self.tabs[name]

    def add_note_tab(self) -> None:
        buttons = [manual('tools/notes')]
        if is_authorized('contributor'):
            buttons.append(
                button(
                    _('note'),
                    url_for('note_insert', entity_id=self.entity.id)))
        self.tabs['note'] = Tab('note', buttons=buttons, entity=self.entity)
        for note in current_user.get_notes_by_entity_id(self.entity.id):
            data = [
                format_date(note['created']),
                _('public') if note['public'] else _('private'),
                link(User.get_by_id(note['user_id'])),
                note['text'],
                link(_('view'), url_for('note_view', id_=note['id']))]
            self.tabs['note'].table.rows.append(data)

    def add_buttons(self) -> None:
        self.buttons = []
        if manual_link := manual(f"entity/{self.entity.class_.group['name']}"):
            self.buttons.append(manual_link)
        if self.entity.class_.name == 'source_translation':
            self.buttons = [manual('entity/source')]
        self.add_button_update()
        self.add_button_delete()
        for item in self.entity.class_.display['buttons']:
            match item:
                case 'copy' if is_authorized(self.entity.class_.write_access):
                    self.buttons.append(
                        button(
                            _('copy'),
                            url_for(
                                'update',
                                id_=self.entity.id,
                                copy='copy_')))

                case 'download':
                    if path := get_file_path(self.entity.id):
                        self.buttons.append(
                            button(
                                _('download'),
                                url_for('download', filename=path.name)))
                    else:
                        self.buttons.append(
                            '<span class="error">'
                            + uc_first(_("missing file")) + '</span>')
                case 'network':
                    self.buttons.append(
                        button(
                            _('network'),
                            url_for(
                                'network',
                                dimensions=0,
                                id_=self.entity.id)))
                case 'selectable' if is_authorized('editor'):
                    self.add_button_selectable()
                case 'stratigraphic_tools' if is_authorized('editor'):
                    self.buttons.append(
                        button(
                            _('tools'),
                            url_for('tools_index', id_=self.entity.id)))
        self.buttons.append(bookmark_toggle(self.entity.id))
        self.buttons.append(
            render_template('util/api_links.html', entity=self.entity))

    def add_button_selectable(self) -> None:
        if not self.entity.selectable:
            self.buttons.append(
                button(
                    _('set selectable'),
                    url_for('type_set_selectable', id_=self.entity.id)))
        elif not self.entity.count and self.entity.category != 'value':
            self.buttons.append(
                button(
                    _('set unselectable'),
                    url_for('type_unset_selectable', id_=self.entity.id)))

    def add_button_delete(self) -> None:
        from openatlas.views.entity import deletion_possible
        if not deletion_possible(self.entity):
            return
        msg = _(
            'Delete %(name)s?',
            name=escape(self.entity.name.replace('\'', '')))
        self.buttons.append(button(
            _('delete'),
            url_for('delete', id_=self.entity.id),
            onclick=f"return confirm('{msg}')"))

    def add_button_update(self) -> None:
        if not is_authorized(self.entity.class_.write_access) \
                or self.problematic_type:
            return
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
        if self.entity.class_.group['name'] == 'actor' \
                and not (self.entity.dates.first and self.entity.dates.last):
            appears_first, appears_last = get_appearance(self.entity)
            self.data[_('appears first')] = appears_first
            self.data[_('appears last')] = appears_last
        if self.entity.standard_type:
            var = ' > '.join(
                [g.types[id_].name for id_ in self.entity.standard_type.root])
            self.data[_('type')] = \
                f'<span title="{var}">{link(self.entity.standard_type)}</span>'
        self.data.update(self.get_type_data())
        for name, attribute in self.entity.class_.attributes.items():
            if name in [
                    'creator', 'example_id', 'license_holder', 'public',
                    'resolver_url', 'website_url']:
                if value := getattr(self.entity, name):
                    if isinstance(value, bool):
                        value = display_bool(value)
                        if name == 'public' \
                                and value \
                                and not self.entity.standard_type:
                            value += (
                                ' <span class="error">'
                                + _('but license is missing ')
                                + '</span>')
                    elif attribute.get('format') == 'url':
                        value = link(value, value, external=True)
                    self.data[attribute['label']] = str(value)
        for name, relation in self.entity.class_.relations.items():
            if relation.mode in ['direct', 'display']:
                self.data[relation.label] = []
                for e in self.entity.get_linked_entities(
                        relation.property,
                        relation.classes,
                        relation.inverse):
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
                        self.data[relation.label].append(link(e))
        for name, item in \
                self.entity.class_.display['additional_information'].items():
            match name:
                case 'file_extension':
                    self.data[item['label']] = self.entity.get_file_ext()
                case 'file_size':
                    self.data[item['label']] = self.entity.get_file_size()
                case 'type_information':
                    if self.entity.category == 'value':
                        self.data[_('unit')] = self.entity.description
                    self.data[_('selectable')] = display_bool(
                        self.entity.selectable)
                    self.data[_('ID for imports')] = self.entity.id
