from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from flask import g, url_for
from flask_babel import lazy_gettext as _
from flask_wtf import FlaskForm

from openatlas.display.table import Table
from openatlas.display.util import (
    button, check_iiif_activation, check_iiif_file_exist)
from openatlas.display.util2 import is_authorized, manual, uc_first

if TYPE_CHECKING:  # pragma: no cover
    from openatlas.models.entity import Entity


class Tab:

    def __init__(
            self,
            name: str,
            label: Optional[str] = None,
            content: Optional[str] = None,
            table: Optional[Table] = None,
            buttons: Optional[list[str]] = None,
            entity: Optional[Entity] = None,
            form: Optional[FlaskForm] = None,
            tooltip: Optional[str] = None) -> None:

        self.name = name
        self.label = uc_first(label or _(name))
        self.content = content
        self.entity = entity
        self.form = form
        self.table = table or Table()
        self.set_table_headers(name, entity)
        self.buttons: list[str] = buttons or [manual(f'entity/{name}')]
        self.tooltip = uc_first(tooltip) if tooltip else ''
        if is_authorized('contributor'):
            self.set_buttons(name, entity)

    def set_table_headers(
            self,
            name: str,
            entity: Optional[Entity] = None) -> None:
        view = entity.class_.view if entity else None
        if entity and not self.table.header:
            self.table.header = g.table_headers[name]
        if name == 'reference' or entity and entity.class_.view == 'reference':
            self.table.header = self.table.header + ['page']
        match name:
            case 'actor' if view == 'place':
                self.table.header = [
                    'actor',
                    'property',
                    'class',
                    'first',
                    'last',
                    'description']
            case 'actor' if view == 'event':
                self.table.header = [
                    'actor',
                    'class',
                    'involvement',
                    'first',
                    'last',
                    'description']
            case 'event' if view == 'actor':
                self.table.header = [
                    'event',
                    'class',
                    'involvement',
                    'first',
                    'last',
                    'description']
            case 'file' if view != 'reference':
                self.table.header += [_('main image')]
            case 'subs':
                self.table.header = [_('name'), _('count'), _('info')]
                if view == 'event':
                    self.table.header = g.table_headers['event']

    def set_buttons(self, name: str, entity: Optional[Entity] = None) -> None:
        view = entity.class_.view if entity else None
        id_ = entity.id if entity else None
        class_name = entity.class_.name if entity else None
        match name:
            case 'actor':
                match view:
                    case 'file':
                        self.buttons.append(
                            button(
                                'link',
                                url_for('file_add', id_=id_, view='actor')))
                    case 'reference':
                        self.buttons.append(
                            button(
                                'link',
                                url_for(
                                    'reference_add',
                                    id_=id_,
                                    view='actor')))
                    case 'source':
                        self.buttons.append(
                            button(
                                'link',
                                url_for('link_insert', id_=id_, view='actor')))
                    case 'event':
                        self.buttons.append(button(
                            'link',
                            url_for(
                                'insert_relation',
                                type_='involvement',
                                origin_id=id_)))
                for item in g.view_class_mapping['actor']:
                    self.buttons.append(
                        button(
                            g.classes[item].label,
                            url_for('insert', class_=item, origin_id=id_)))
            case 'artifact':
                if class_name == 'source':
                    self.buttons.append(
                        button(
                            'link',
                            url_for('link_insert', id_=id_, view='artifact')))
                if class_name in [
                        'place',
                        'artifact',
                        'human_remains',
                        'feature',
                        'stratigraphic_unit']:
                    self.buttons.append(
                        button(
                            _('add subunit'),
                            url_for('add_subunit', super_id=id_)))
                if class_name != 'human_remains':
                    self.buttons.append(
                        button(
                            g.classes['artifact'].label,
                            url_for(
                                'insert',
                                class_='artifact',
                                origin_id=id_)))
                if class_name != 'artifact':
                    self.buttons.append(
                        button(
                            g.classes['human_remains'].label,
                            url_for(
                                'insert',
                                class_='human_remains',
                                origin_id=id_)))
            case 'event':
                match view:
                    case 'file':
                        self.buttons.append(
                            button(
                                'link',
                                url_for('file_add', id_=id_, view='event')))
                    case 'actor':
                        self.buttons.append(
                            button(
                                'link',
                                url_for(
                                    'insert_relation',
                                    type_='involvement',
                                    origin_id=id_)))
                    case 'source':
                        self.buttons.append(
                            button(
                                'link',
                                url_for('link_insert', id_=id_, view='event')))
                    case 'reference':
                        self.buttons.append(
                            button(
                                'link',
                                url_for(
                                    'reference_add',
                                    id_=id_,
                                    view='event')))
                    case 'artifact':
                        for item in [
                                'acquisition',
                                'modification',
                                'move',
                                'production']:
                            self.buttons.append(
                                button(
                                    g.classes[item].label,
                                    url_for(
                                        'insert',
                                        class_=item,
                                        origin_id=id_),
                                    tooltip_text=g.classes[item].
                                    get_tooltip()))
                    case _:
                        for item in g.view_class_mapping['event']:
                            self.buttons.append(
                                button(
                                    g.classes[item].label,
                                    url_for(
                                        'insert',
                                        class_=item,
                                        origin_id=id_),
                                    tooltip_text=g.classes[item]
                                    .get_tooltip()))
            case 'feature' if class_name == 'place':
                self.buttons.append(
                    button(
                        g.classes[name].label,
                        url_for('insert', class_=name, origin_id=id_)))
            case 'file':
                if view == 'reference':
                    self.buttons.append(
                        button(
                            'link',
                            url_for('reference_add', id_=id_, view=name)))
                else:
                    self.buttons.append(
                        button('link', url_for('entity_add_file', id_=id_)))
                self.buttons.append(
                    button(
                        g.classes[name].label,
                        url_for('insert', class_=name, origin_id=id_)))
                if entity and check_iiif_activation():
                    for file in entity.get_linked_entities('P67', True):
                        if (file.class_.view == 'file'
                                and check_iiif_file_exist(file.id)):
                            self.buttons.append(
                                button(
                                    _('view all IIIF images'),
                                    url_for('view_iiif', id_=entity.id)))
                            break
            case 'member':
                self.buttons.append(
                    button(
                        'link',
                        url_for(
                            'insert_relation',
                            type_='member',
                            origin_id=id_)))
            case 'member_of':
                self.buttons.append(
                    button(
                        'link',
                        url_for(
                            'insert_relation',
                            type_='membership',
                            origin_id=id_)))
            case 'note' if is_authorized('contributor'):
                self.buttons.append(
                    button(_('note'), url_for('note_insert', entity_id=id_)))
            case 'place':
                if class_name == 'file':
                    self.buttons.append(
                        button(
                            'link',
                            url_for('file_add', id_=id_, view=name)))
                elif view == 'reference':
                    self.buttons.append(
                        button(
                            'link',
                            url_for('reference_add', id_=id_, view=name)))
                elif view == 'source':
                    self.buttons.append(
                        button(
                            'link',
                            url_for('link_insert', id_=id_, view=name)))
                self.buttons.append(
                    button(
                        g.classes[name].label,
                        url_for('insert', class_=name, origin_id=id_)))
            case 'reference':
                self.buttons.append(
                    button('link', url_for('entity_add_reference', id_=id_)))
                for item in g.view_class_mapping['reference']:
                    self.buttons.append(
                        button(
                            g.classes[item].label,
                            url_for('insert', class_=item, origin_id=id_)))
            case 'relation':
                self.buttons.append(
                    button(
                        'link',
                        url_for(
                            'insert_relation',
                            type_='actor_relation',
                            origin_id=id_)))
                for item in g.view_class_mapping['actor']:
                    self.buttons.append(
                        button(
                            g.classes[item].label,
                            url_for('insert', class_=item, origin_id=id_)))
            case 'source':
                if class_name == 'file':
                    self.buttons.append(
                        button(
                            _('link'),
                            url_for('file_add', id_=id_, view=name)))
                elif view == 'reference':
                    self.buttons.append(
                        button(
                            'link',
                            url_for('reference_add', id_=id_, view=name)))
                else:
                    self.buttons.append(
                        button('link', url_for('entity_add_source', id_=id_)))
                self.buttons.append(
                    button(
                        g.classes['source'].label,
                        url_for('insert', class_=name, origin_id=id_)))
            case 'stratigraphic_unit' if class_name == 'feature':
                self.buttons.append(
                    button(
                        g.classes['stratigraphic_unit'].label,
                        url_for('insert', class_=name, origin_id=id_)))
            case 'text':
                self.buttons.append(button(
                    _('text'),
                    url_for(
                        'insert',
                        class_='source_translation',
                        origin_id=id_)))
