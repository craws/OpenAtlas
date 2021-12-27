from typing import List, Optional, TYPE_CHECKING, Union

from flask import g, url_for
from flask_babel import lazy_gettext as _
from flask_login import current_user

from openatlas.models.openatlas_class import OpenatlasClass
from openatlas.util.table import Table
from openatlas.util.util import button, is_authorized, uc_first

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
_('circular dependencies')


class Tab:

    def __init__(
            self,
            name: str,
            content: Optional[str] = None,
            table: Optional[Table] = None,
            buttons: Optional[List[str]] = None,
            entity: Optional['Entity'] = None) -> None:

        self.name = name
        self.content = content
        self.title = uc_first(_(name.replace('_', ' ')))
        self.entity = entity
        self.table = table if table else Table()
        id_ = None
        view = None
        class_ = None
        if entity:
            id_ = entity.id
            view = entity.class_.view
            class_ = entity.class_
            if not self.table.header:
                self.table.header = g.table_headers[name]
        if name == 'reference' or entity and entity.class_.view == 'reference':
            self.table.header = self.table.header + ['page']

        buttons = buttons if buttons else []
        self.add_buttons(name, buttons, view, id_, class_)
        self.buttons = buttons \
            if buttons and is_authorized('contributor') else []

    def add_buttons(
            self,
            name: str,
            buttons: List[str],
            view: Union[None, str],
            id_: Union[None, int],
            class_: Union[None, OpenatlasClass]) -> None:

        if name == 'actor':
            if view == 'place':
                self.table.header = [
                    'actor',
                    'property',
                    'class',
                    'first',
                    'last',
                    'description']
            elif view == 'file':
                buttons += [
                    button('link', url_for('file_add', id_=id_, view=name))]
            elif view == 'reference':
                buttons += [button(
                    'link',
                    url_for('reference_add', id_=id_, view=name))]
            elif view == 'source':
                buttons += [
                    button('link', url_for('link_insert', id_=id_, view=name))]
            elif view == 'event':
                self.table.header = [
                    'actor',
                    'class',
                    'involvement',
                    'first',
                    'last',
                    'description']
                buttons += [button(
                    'link',
                    url_for('involvement_insert', origin_id=id_))]
            for item in g.view_class_mapping['actor']:
                buttons.append(button(
                    g.classes[item].label,
                    url_for('insert', class_=item, origin_id=id_)))
        elif name == 'artifact':
            if class_.name != 'stratigraphic_unit':
                buttons += [
                    button(
                        'link',
                        url_for('link_insert', id_=id_, view='artifact'))]
            buttons += [
                button(
                    g.classes[name].label,
                    url_for('insert', class_=name, origin_id=id_))]
        elif name == 'entities':
            if id_:
                buttons += [button(
                    _('move entities'),
                    url_for('type_move_entities', id_=id_))]
        elif name == 'event':
            if view == 'file':
                buttons += [
                    button('link', url_for('file_add', id_=id_, view='event'))]
            elif view == 'actor':
                self.table.header = [
                    'event',
                    'class',
                    'involvement',
                    'first',
                    'last', 'description']
                buttons += [button(
                    'link',
                    url_for('involvement_insert', origin_id=id_))]
            elif view == 'source':
                buttons += [button(
                    'link',
                    url_for('link_insert', id_=id_, view='event'))]
            elif view == 'reference':
                buttons += [button(
                    'link',
                    url_for('reference_add', id_=id_, view='event'))]
            if view == 'artifact':
                for item in ['move', 'production']:
                    buttons += [button(
                        g.classes[item].label,
                        url_for('insert', class_=item, origin_id=id_))]
            else:
                for item in g.view_class_mapping['event']:
                    buttons.append(button(
                        g.classes[item].label,
                        url_for('insert', class_=item, origin_id=id_)))
        elif name == 'feature':
            if current_user.settings['module_sub_units'] \
                    and class_.name == 'place':
                buttons += [button(
                    g.classes[name].label,
                    url_for('insert', class_=name, origin_id=id_))]
        elif name == 'file':
            if view == 'reference':
                buttons += [button(
                    'link',
                    url_for('reference_add', id_=id_, view=name))]
            else:
                self.table.header += [_('main image')]
                buttons += [button('link', url_for('entity_add_file', id_=id_))]
            buttons.append(button(
                g.classes[name].label,
                url_for('insert', class_=name, origin_id=id_)))
        elif name == 'human_remains':
            if current_user.settings['module_sub_units'] \
                    and class_.name == 'stratigraphic_unit':
                buttons += [button(
                    g.classes[name].label,
                    url_for('insert', origin_id=id_, class_=name))]
        elif name == 'member':
            buttons += [button('link', url_for('member_insert', origin_id=id_))]
        elif name == 'member_of':
            buttons += [button(
                'link',
                url_for('member_insert', origin_id=id_, code='membership'))]
        elif name == 'note':
            if is_authorized('contributor'):
                buttons += [
                    button(_('note'), url_for('note_insert', entity_id=id_))]
        elif name == 'place':
            if class_.name == 'file':
                buttons += [
                    button('link', url_for('file_add', id_=id_, view=name))]
            elif view == 'reference':
                buttons += [button(
                    'link',
                    url_for('reference_add', id_=id_, view=name))]
            elif view == 'source':
                buttons += [
                    button('link', url_for('link_insert', id_=id_, view=name))]
            buttons.append(button(
                g.classes[name].label,
                url_for('insert', class_=name, origin_id=id_)))
        elif name == 'reference':
            buttons += [
                button('link', url_for('entity_add_reference', id_=id_))]
            for item in g.view_class_mapping['reference']:
                buttons.append(button(
                    g.classes[item].label,
                    url_for('insert', class_=item, origin_id=id_)))
        elif name == 'relation':
            buttons += [
                button('link', url_for('relation_insert', origin_id=id_))]
            for item in g.view_class_mapping['actor']:
                buttons.append(button(
                    g.classes[item].label,
                    url_for('insert', class_=item, origin_id=id_)))
        elif name == 'source':
            if class_.name == 'file':
                buttons += [
                    button(_('link'), url_for('file_add', id_=id_, view=name))]
            elif view == 'reference':
                buttons += [button(
                    'link',
                    url_for('reference_add', id_=id_, view=name))]
            else:
                buttons += [
                    button('link', url_for('entity_add_source', id_=id_))]
            buttons.append(button(
                g.classes['source'].label,
                url_for('insert', class_=name, origin_id=id_)))
        elif name == 'subs':
            self.table.header = [_('name'), _('count'), _('info')]
            if view == 'event':
                self.table.header = g.table_headers['event']
        elif name == 'stratigraphic_unit':
            if current_user.settings['module_sub_units'] \
                    and class_.name == 'feature':
                buttons += [button(
                    g.classes['stratigraphic_unit'].label,
                    url_for('insert', class_=name, origin_id=id_))]
        elif name == 'text':
            buttons += [button(
                _('text'),
                url_for('insert', class_='source_translation', origin_id=id_))]
