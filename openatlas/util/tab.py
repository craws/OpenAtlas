from typing import List, Optional

from flask import g, url_for
from flask_babel import format_number, lazy_gettext as _
from flask_login import current_user

from openatlas.models.entity import Entity
from openatlas.util.display import button, uc_first
from openatlas.util.table import Table
from openatlas.util.util import is_authorized

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

# Needed for translations of content items
_('intro_for_frontend')
_('legal_notice_for_frontend')
_('contact_for_frontend')


def tab_header(id_: str, table: Optional[Table] = None, active: Optional[bool] = False) -> str:
    label = uc_first(_(id_.replace('_', ' ').replace('-', ' ').lower()))
    label += ' <span class="tab-counter">{counter}</span>'.format(
        counter=format_number(len(table.rows))) if table and len(table.rows) else ''
    return '''
        <li class="nav-item">
            <a 
                class="nav-link {active}" 
                data-toggle="tab" 
                role="tab" 
                aria-selected="{selected}" 
                href="#tab-{id}">{label}
            </a>
        </li>'''.format(active=' active' if active else '',
                        selected='true' if active else 'false',
                        label=label,
                        id=id_.replace('_', '-').replace(' ', '-'))


class Tab:
    origin: Optional[Entity]
    buttons: Optional[List[str]]
    table: Table

    def __init__(self, name: str, origin: Optional[Entity] = None) -> None:
        self.name = name
        self.title = uc_first(_(name.replace('_', ' ')))
        self.origin = origin
        if not origin:
            return

        id_ = origin.id
        buttons: List[str] = []
        table = Table(g.table_headers[name])
        view_name = origin.class_.view
        class_name = origin.class_.name

        if name == 'reference':
            table.header = table.header + ['page']
        if name == 'actor':
            if view_name == 'place':
                table.header = ['actor', 'property', 'class', 'first', 'last', 'description']
            elif view_name == 'file':
                buttons = [button('link', url_for('file_add', id_=id_, class_name='actor'))]
            elif view_name == 'reference':
                buttons = [button('link', url_for('reference_add', id_=id_, class_name='actor'))]
            elif view_name == 'source':
                buttons = [button('link', url_for('source_add', id_=id_, class_name='actor'))]
            elif view_name == 'event':
                table.header = ['actor', 'class', 'involvement', 'first', 'last', 'description']
                buttons = [button('link', url_for('involvement_insert', origin_id=id_))]
            for item in g.view_class_mapping['actor']:
                buttons.append(button(item, url_for('insert', class_=item, origin_id=id_)))
        elif name == 'entities':
            buttons = [button(_('move entities'), url_for('node_move_entities', id_=id_))]
        elif name == 'event':
            if view_name == 'file':
                buttons = [button('link', url_for('file_add', id_=id_, class_name='event'))]
            elif view_name == 'actor':
                table.header = ['event', 'class', 'involvement', 'first', 'last', 'description']
                buttons = [button('link', url_for('involvement_insert', origin_id=id_))]
            elif view_name == 'source':
                buttons = [button('link', url_for('source_add', id_=id_, class_name='event'))]
            elif view_name == 'reference':
                buttons = [button('link', url_for('reference_add', id_=id_, class_name='event'))]
            for item in g.view_class_mapping['event']:
                buttons.append(button(item, url_for('insert', class_=item, origin_id=id_)))
            if view_name == 'artifact':
                buttons = [button('move', url_for('insert', class_='move', origin_id=id_))]
        elif name == 'feature':
            if current_user.settings['module_sub_units'] and class_name == 'place':
                buttons = [button('feature', url_for('insert', class_='feature', origin_id=id_))]
        elif name == 'find':
            if current_user.settings['module_sub_units'] and class_name == 'stratigraphic_unit':
                buttons = [button(_('find'), url_for('insert', class_='find', origin_id=id_))]
        elif name == 'file':
            if view_name == 'reference':
                buttons = [button('link', url_for('reference_add', id_=id_, class_name='file'))]
            else:
                table.header += [_('main image')]
                buttons = [button('link', url_for('entity_add_file', id_=id_))]
            buttons.append(button('file', url_for('insert', class_='file', origin_id=id_)))
        elif name == 'human_remains':
            if current_user.settings['module_sub_units'] and class_name == 'stratigraphic_unit':
                buttons = [button('human remains', url_for('insert',
                                                           origin_id=id_,
                                                           class_='human_remains'))]
        elif name == 'member':
            buttons = [button('link', url_for('member_insert', origin_id=id_))]
        elif name == 'member_of':
            buttons = [button('link', url_for('member_insert', origin_id=id_, code='membership'))]
        elif name == 'place':
            if class_name == 'file':
                buttons = [button('link', url_for('file_add', id_=id_, class_name='place'))]
            elif view_name == 'reference':
                buttons = [button('link', url_for('reference_add', id_=id_, class_name='place'))]
            elif view_name == 'source':
                buttons = [button('link', url_for('source_add', id_=id_, class_name='place'))]
            buttons.append(button('place', url_for('insert', class_='place', origin_id=id_)))
        elif name == 'reference':
            buttons = [button('link', url_for('entity_add_reference', id_=id_))]
            for item in g.view_class_mapping['reference']:
                buttons.append(button(item, url_for('insert', class_=item, origin_id=id_)))
        elif name == 'relation':
            buttons = [button('link', url_for('relation_insert', origin_id=id_))]
            for item in g.view_class_mapping['actor']:
                buttons.append(button(item, url_for('insert', class_=item, origin_id=id_)))
        elif name == 'source':
            if class_name == 'file':
                buttons = [button(_('link'), url_for('file_add', id_=id_, class_name='source'))]
            elif view_name == 'reference':
                buttons = [button('link', url_for('reference_add', id_=id_, class_name='source'))]
            else:
                buttons = [button('link', url_for('entity_add_source', id_=id_))]
            buttons.append(button('source', url_for('insert', class_='source', origin_id=id_)))
        elif name == 'subs':
            table.header = [_('name'), _('count'), _('info')]
            if view_name == 'event':
                table.header = g.table_headers['event']
        elif name == 'stratigraphic_unit':
            if current_user.settings['module_sub_units'] and class_name == 'feature':
                buttons = [button(_('stratigraphic unit'), url_for('insert',
                                                                   class_='stratigraphic_unit',
                                                                   origin_id=id_))]
        elif name == 'text':
            buttons = [button(_('text'), url_for('translation_insert', source_id=id_))]

        self.table = table
        if is_authorized('contributor'):
            self.buttons = buttons
