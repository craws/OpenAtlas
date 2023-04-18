from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from flask import g, url_for
from flask_babel import lazy_gettext as _
from flask_wtf import FlaskForm

from openatlas.display.table import Table
from openatlas.display.util import button, is_authorized

if TYPE_CHECKING:  # pragma: no cover
    from openatlas.models.entity import Entity

# Needed for translations of tab titles
_('member of')
_('texts')
_('invalid dates')
_('invalid link dates')
_('invalid involvement dates')
_('unlinked')
_('missing files')
_('orphaned files')
_('orphaned subunits')
_('circular dependencies')


class Tab:

    def __init__(
            self,
            name: str,
            content: Optional[str] = None,
            table: Optional[Table] = None,
            buttons: Optional[list[str]] = None,
            entity: Optional[Entity] = None,
            form: Optional[FlaskForm] = None) -> None:

        self.name = name
        self.content = content
        self.entity = entity
        self.table = table or Table()
        self.set_table_headers(name, entity)
        self.buttons: list[str] = []
        self.form = form
        if is_authorized('contributor') or name == 'files':
            self.set_buttons(name, buttons, entity)

    def set_table_headers(
            self,
            name: str,
            entity: Optional[Entity] = None) -> None:
        view = entity.class_.view if entity else None
        if entity:
            if not self.table.header:
                self.table.header = g.table_headers[name]
        if name == 'reference' or entity and entity.class_.view == 'reference':
            self.table.header = self.table.header + ['page']
        if name == 'actor':
            if view == 'place':
                self.table.header = [
                    'actor',
                    'property',
                    'class',
                    'first',
                    'last',
                    'description']
            elif view == 'event':
                self.table.header = [
                    'actor',
                    'class',
                    'involvement',
                    'first',
                    'last',
                    'description']
        elif name == 'event':
            if view == 'actor':
                self.table.header = [
                    'event',
                    'class',
                    'involvement',
                    'first',
                    'last', 'description']
        elif name == 'file':
            if view != 'reference':
                self.table.header += [_('main image')]
        elif name == 'subs':
            self.table.header = [_('name'), _('count'), _('info')]
            if view == 'event':
                self.table.header = g.table_headers['event']

    def set_buttons(
            self,
            name: str,
            buttons: Optional[list[str]],
            entity: Optional[Entity] = None) -> None:
        view = entity.class_.view if entity else None
        id_ = entity.id if entity else None
        class_ = entity.class_ if entity else None
        self.buttons = buttons or []
        if name == 'actor':
            if view == 'file':
                self.buttons.append(
                    button('link', url_for('file_add', id_=id_, view=name)))
            elif view == 'reference':
                self.buttons.append(
                    button(
                        'link',
                        url_for('reference_add', id_=id_, view=name)))
            elif view == 'source':
                self.buttons.append(
                    button('link', url_for('link_insert', id_=id_, view=name)))
            elif view == 'event':
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
        elif name == 'artifact':
            self.buttons.append(
                button(_('add subunit'), url_for('add_subunit', super_id=id_)))
            if entity and entity.class_.name != 'human_remains':
                self.buttons.append(
                    button(
                        g.classes['artifact'].label,
                        url_for('insert', class_='artifact', origin_id=id_)))
            if entity and entity.class_.name != 'artifact':
                self.buttons.append(
                    button(
                        g.classes['human_remains'].label,
                        url_for(
                            'insert',
                            class_='human_remains',
                            origin_id=id_)))
        elif name == 'entities':
            if id_ and id_ in g.types:
                type_ = g.types[id_]
                root = g.types[type_.root[0]] if type_.root else type_
                if root.category not in ['system', 'value']:
                    self.buttons.append(
                        button(
                            _('move entities'),
                            url_for('type_move_entities', id_=id_)))
        elif name == 'event':
            if view == 'file':
                self.buttons.append(
                    button('link', url_for('file_add', id_=id_, view='event')))
            elif view == 'actor':
                self.buttons.append(
                    button(
                        'link',
                        url_for(
                            'insert_relation',
                            type_='involvement',
                            origin_id=id_)))
            elif view == 'source':
                self.buttons.append(
                    button(
                        'link',
                        url_for('link_insert', id_=id_, view='event')))
            elif view == 'reference':
                self.buttons.append(
                    button(
                        'link',
                        url_for('reference_add', id_=id_, view='event')))
            if view == 'artifact':
                for item in ['acquisition', 'move', 'production']:
                    self.buttons.append(
                        button(
                            g.classes[item].label,
                            url_for('insert', class_=item, origin_id=id_),tooltip_text=g.classes[item].get_tooltip()))
            else:
                for item in g.view_class_mapping['event']:
                    self.buttons.append(
                        button(
                            g.classes[item].label,
                            url_for('insert', class_=item, origin_id=id_),tooltip_text=g.classes[item].get_tooltip()))
        elif name == 'feature':
            if class_ and class_.name == 'place':
                self.buttons.append(
                    button(
                        g.classes[name].label,
                        url_for('insert', class_=name, origin_id=id_)))
        elif name == 'file':
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
        elif name == 'member':
            self.buttons.append(
                button(
                    'link',
                    url_for('insert_relation', type_='member', origin_id=id_)))
        elif name == 'member_of':
            self.buttons.append(button(
                'link',
                url_for('insert_relation', type_='membership', origin_id=id_)))
        elif name == 'note' and is_authorized('contributor'):
            self.buttons.append(
                button(_('note'), url_for('note_insert', entity_id=id_)))
        elif name == 'place':
            if class_ and class_.name == 'file':
                self.buttons.append(
                    button('link', url_for('file_add', id_=id_, view=name)))
            elif view == 'reference':
                self.buttons.append(
                    button(
                        'link',
                        url_for('reference_add', id_=id_, view=name)))
            elif view == 'source':
                self.buttons.append(
                    button('link', url_for('link_insert', id_=id_, view=name)))
            self.buttons.append(
                button(
                    g.classes[name].label,
                    url_for('insert', class_=name, origin_id=id_)))
        elif name == 'reference':
            self.buttons.append(
                button('link', url_for('entity_add_reference', id_=id_)))
            for item in g.view_class_mapping['reference']:
                self.buttons.append(button(
                    g.classes[item].label,
                    url_for('insert', class_=item, origin_id=id_)))
        elif name == 'relation':
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
        elif name == 'source':
            if class_ and class_.name == 'file':
                self.buttons.append(
                    button(_('link'), url_for('file_add', id_=id_, view=name)))
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
        elif name == 'stratigraphic_unit':
            if class_ and class_.name == 'feature':
                self.buttons.append(
                    button(
                        g.classes['stratigraphic_unit'].label,
                        url_for('insert', class_=name, origin_id=id_)))
        elif name == 'text':
            self.buttons.append(button(
                _('text'),
                url_for('insert', class_='source_translation', origin_id=id_)))
